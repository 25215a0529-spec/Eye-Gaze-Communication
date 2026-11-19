"""Full-screen calibration: 12 dots (each of the 6 card positions twice),
then shows the measured accuracy for a few seconds."""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen
from core.eye_tracker import CALIB_GRID
from ui.theme import CARD_PALETTE

DOT_MS = 1600        # time per dot
RESULT_MS = 3500     # how long the accuracy result stays on screen

# Instruction screen shown before the dots: short, simple words in 3 languages.
# Each entry = (two lines of text, text colour). Edit the words here.
INSTRUCTIONS = [
    (["మీ తలను కదపకండి.", "ప్రతి చుక్కను కళ్లతో చూడండి."], CARD_PALETTE[0]),            # Telugu
    (["Keep your head still.", "Follow each dot with your eyes."], CARD_PALETTE[1]),      # English
    (["अपना सिर स्थिर रखें।", "हर बिंदु को आँखों से देखें।"], CARD_PALETTE[2]),            # Hindi
]
INSTRUCTION_FONTS = ["Nirmala UI", "Noto Sans Telugu", "Noto Sans Devanagari", "Segoe UI", "Arial"]
INSTRUCTION_SIZE = 0.045      # text height as a fraction of the screen height (bigger = larger text)


class CalibrationOverlay(QWidget):
    finished = pyqtSignal(object)   # accuracy 0..1, or None if failed

    def __init__(self, tracker, sw, sh):
        super().__init__()
        self.tracker, self.sw, self.sh = tracker, sw, sh
        self.idx = -1
        self.result_text = ""
        self.result_color = "#94a3b8"
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background:#0b1220;")
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._next)

    def start(self):
        self.tracker.recalibrate()
        self.idx = -1
        self.result_text = ""
        self.showFullScreen()
        self.update()
        QTimer.singleShot(1800, self._next)   # time to get ready

    def _next(self):
        self.tracker.hide_dot()
        self.idx += 1
        if self.idx >= len(CALIB_GRID):
            acc = self.tracker.finish_calibration(self.sw, self.sh)
            if acc is None:
                self.result_text = self.tracker.report_text + "\nPress C to try again."
                self.result_color = "#f87171"
            else:
                hint = ""
                if acc < 0.6:
                    hint = "\nLow accuracy: face a light, sit 50-60 cm away, keep your head still,\nthen press C to calibrate again."
                    self.result_color = "#fbbf24"
                else:
                    self.result_color = "#4ade80"
                self.result_text = self.tracker.report_text + hint
            self._acc = acc
            self.update()
            QTimer.singleShot(RESULT_MS, self._close_and_emit)
            return
        self.tracker.show_dot(self.idx, self.sw, self.sh)
        self.update()
        self.timer.start(DOT_MS)

    def _close_and_emit(self):
        self.close()
        self.finished.emit(getattr(self, "_acc", None))

    def _draw_instructions(self, p):
        """Bold, centred instructions in Telugu, English and Hindi, sized to the screen."""
        w, h = self.width(), self.height()
        size = max(26, int(h * INSTRUCTION_SIZE))

        # shrink only if the longest line would not fit across the screen
        while True:
            font = QFont()
            font.setFamilies(INSTRUCTION_FONTS)
            font.setBold(True)
            font.setPixelSize(size)
            fm = QFontMetrics(font)
            longest = max(fm.horizontalAdvance(t) for lines, _ in INSTRUCTIONS for t in lines)
            if longest <= w * 0.88 or size <= 20:
                break
            size -= 2

        p.setFont(font)
        line_h = int(size * 1.45)
        gap = int(size * 0.9)
        n_lines = sum(len(lines) for lines, _ in INSTRUCTIONS)
        total = n_lines * line_h + (len(INSTRUCTIONS) - 1) * gap
        y = (h - total) // 2

        for i, (lines, color) in enumerate(INSTRUCTIONS):
            p.setPen(QColor(color))
            for text in lines:
                p.drawText(QRect(0, y, w, line_h), Qt.AlignmentFlag.AlignCenter, text)
                y += line_h
            if i < len(INSTRUCTIONS) - 1:          # thin divider between languages
                p.setPen(QPen(QColor("#2C3240"), 2))
                p.drawLine(w // 2 - 70, y + gap // 2, w // 2 + 70, y + gap // 2)
                y += gap

    def paintEvent(self, _):
        p = QPainter(self)
        p.setFont(QFont("Arial", 18))
        p.setPen(QColor("#94a3b8"))
        if self.idx < 0:
            self._draw_instructions(p)
            return
        if self.idx >= len(CALIB_GRID):
            p.setPen(QColor(self.result_color))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.result_text)
            return
        fx, fy = CALIB_GRID[self.idx]
        cx, cy = int(fx * self.width()), int(fy * self.height())
        p.setBrush(QColor("#22d3ee"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(cx - 18, cy - 18, 36, 36)
        p.setBrush(QColor("#0b1220"))
        p.drawEllipse(cx - 5, cy - 5, 10, 10)