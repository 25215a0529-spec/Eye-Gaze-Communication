import threading
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import QTimer, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QPainterPath

from ui.theme import (
    CARD_PALETTE, CARD_TEXT, BORDER_IDLE, BORDER_FOCUS,
    BORDER_SELECTED, RING_COLOR, UI_FONT,
)

try:
    import winsound
except ImportError:
    winsound = None

CONFIRM_MS = 450     # how long the "selected" flash is shown before the page changes
CONFIRM_BG = "#8FC9A2"   # soft green flash when a card is selected


def _click_beep():
    """Short high 'tick' so the user HEARS that a card was selected."""
    if winsound is not None:
        threading.Thread(target=lambda: winsound.Beep(1500, 90), daemon=True).start()


class DwellCard(QPushButton):
    # Emits the card's `key` (falls back to the visible text if no key given)
    dwell_completed = pyqtSignal(str)

    def __init__(self, text, key=None, bg_color=CARD_PALETTE[0],
                 text_color=CARD_TEXT, dwell_time_ms=1300,
                 font_px=44, radius=24, parent=None):
        super().__init__(text, parent)
        self.text_label = text                       # what is shown on the card
        self.key = key if key is not None else text  # what is emitted when selected
        self.bg_color = bg_color
        self.text_color = text_color
        self.dwell_time_ms = dwell_time_ms
        self.font_px = font_px
        self.radius = radius
        self.dwell_progress = 0.0
        self.is_locked = False
        self.is_gaze_inside = False
        self.is_confirming = False
        self.is_selected = False

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._apply_style()

        self.clicked.connect(self._manual_click)

        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self._update_dwell)

    def _apply_style(self, focused=False, confirmed=False):
        if confirmed:
            border_color, border_width, bg = BORDER_FOCUS, "10px", CONFIRM_BG
        elif focused:
            border_color, border_width, bg = BORDER_FOCUS, "6px", self.bg_color
        elif self.is_selected:
            border_color, border_width, bg = BORDER_SELECTED, "6px", self.bg_color
        else:
            border_color, border_width, bg = BORDER_IDLE, "2px", self.bg_color
        pressed_bg = QColor(self.bg_color).darker(112).name()
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {self.text_color};
                font-family: {UI_FONT};
                font-size: {self.font_px}px;
                font-weight: bold;
                border-radius: {self.radius}px;
                border: {border_width} solid {border_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_bg};
            }}
        """)

    def set_selected(self, selected: bool):
        """Marks the card as chosen (soft gold outline), e.g. the 'I' card."""
        self.is_selected = selected
        self._apply_style(focused=self.is_gaze_inside)

    def set_locked(self, locked: bool):
        self.is_locked = locked
        if locked:
            self.reset_dwell()

    def start_dwell(self):
        if self.is_locked or self.is_confirming:
            return
        if not self.is_gaze_inside:
            self.is_gaze_inside = True
            self._apply_style(focused=True)
            self.timer.start()

    def reset_dwell(self):
        if self.is_confirming:          # a selection in progress must not be cancelled
            return
        if self.is_gaze_inside or self.dwell_progress > 0.0:
            self.is_gaze_inside = False
            self.timer.stop()
            self.dwell_progress = 0.0
            self._apply_style()
            self.update()

    def _manual_click(self):
        if not self.is_locked and not self.is_confirming:
            self.dwell_completed.emit(self.key)

    def _update_dwell(self):
        if self.is_locked or not self.is_gaze_inside:
            self.reset_dwell()
            return

        self.dwell_progress += 20 / self.dwell_time_ms
        if self.dwell_progress >= 1.0:
            # SELECTED: stop counting, flash green with a tick + beep, then proceed
            self.timer.stop()
            self.dwell_progress = 1.0
            self.is_confirming = True
            self.setText("✓  " + self.text_label)
            self._apply_style(confirmed=True)
            _click_beep()
            self.update()
            QTimer.singleShot(CONFIRM_MS, self._finish_confirm)
            return
        self.update()

    def _finish_confirm(self):
        self.is_confirming = False
        self.is_gaze_inside = False
        self.dwell_progress = 0.0
        self.setText(self.text_label)
        self._apply_style()
        self.dwell_completed.emit(self.key)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.dwell_progress > 0.0 and not self.is_locked and not self.is_confirming:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # soft dark fill that grows left -> right (visible on pastel cards)
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius)
            painter.setClipPath(path)
            painter.fillRect(QRectF(0, 0, self.width() * self.dwell_progress, self.height()),
                             QColor(31, 41, 51, 45))
            painter.setClipping(False)

            # progress ring (only on big cards)
            if self.height() > 90:
                painter.setPen(QPen(QColor(RING_COLOR), 8))
                radius = 26
                cx, cy = self.width() / 2, self.height() - 54
                rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
                painter.drawArc(rect, 90 * 16, int(-self.dwell_progress * 360 * 16))