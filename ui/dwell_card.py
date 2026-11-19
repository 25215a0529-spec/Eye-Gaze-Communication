import threading
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF
from PyQt6.QtGui import (QPainter, QColor, QPen, QFont, QFontMetrics,
                         QPainterPath)

from ui.theme import (
    CARD_PALETTE, CARD_TEXT, BORDER_IDLE, BORDER_FOCUS,
    BORDER_SELECTED, RING_COLOR, UI_FONT,
)
from ui.symbols import get_icon

CONFIRM_BG = "#8FC9A2"     # soft green flash when a card is chosen
CONFIRM_MS = 450

try:
    import winsound
except ImportError:        # not Windows: no beep
    winsound = None


def _families(css_font_stack):
    return [f.strip().strip("'\"") for f in css_font_stack.split(",") if f.strip()]


def _beep():
    if winsound is None:
        return
    threading.Thread(target=lambda: winsound.Beep(880, 120), daemon=True).start()


class DwellCard(QPushButton):
    """A card that is 'clicked' by looking at it for dwell_time_ms.

    - icon: name of a picture in assets/symbols/ (shown above the word).
    - dwell_completed emits `key` (falls back to the text).
    - Everything is painted here, so the picture, word, focus ring and the
      green confirm flash always line up.
    """
    dwell_completed = pyqtSignal(str)

    def __init__(self, text, key=None, bg_color=CARD_PALETTE[0],
                 text_color=CARD_TEXT, dwell_time_ms=1300, font_px=44,
                 radius=24, icon=None, parent=None):
        super().__init__(text, parent)
        self.text_label = text
        self.key = key if key is not None else text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_px = font_px
        self.radius = radius
        self.dwell_time_ms = dwell_time_ms
        self.icon_name = icon
        self.dwell_progress = 0.0
        self.is_locked = False
        self.is_gaze_inside = False
        self.is_selected = False
        self._confirming = False

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)   # keys (Space...) go to the window
        self.clicked.connect(self._manual_click)

        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self._update_dwell)

        self._confirm_timer = QTimer(self)
        self._confirm_timer.setSingleShot(True)
        self._confirm_timer.setInterval(CONFIRM_MS)
        self._confirm_timer.timeout.connect(self._emit_after_confirm)

    # ------------------------------------------------------------ state
    def setText(self, text):
        self.text_label = text
        super().setText(text)
        self.update()

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.update()

    def set_locked(self, locked: bool):
        self.is_locked = locked
        if locked:
            self.reset_dwell()

    def start_dwell(self):
        if self.is_locked or self._confirming:
            return
        if not self.is_gaze_inside:
            self.is_gaze_inside = True
            self.timer.start()
            self.update()

    def reset_dwell(self):
        if self._confirming:
            return
        if self.is_gaze_inside or self.dwell_progress > 0.0:
            self.is_gaze_inside = False
            self.timer.stop()
            self.dwell_progress = 0.0
            self.update()

    # ------------------------------------------------------------ selecting
    def _manual_click(self):
        if not self.is_locked and not self._confirming:
            self._confirm()

    def _update_dwell(self):
        if self.is_locked or not self.is_gaze_inside:
            self.reset_dwell()
            return
        self.dwell_progress += 20 / self.dwell_time_ms
        if self.dwell_progress >= 1.0:
            self.timer.stop()
            self._confirm()
        self.update()

    def _confirm(self):
        self._confirming = True
        self.timer.stop()
        self.dwell_progress = 0.0
        _beep()
        self.update()
        self._confirm_timer.start()

    def _emit_after_confirm(self):
        self.dwell_completed.emit(self.key)
        # if the card is still on screen (e.g. same page), return to normal
        self._confirming = False
        self.is_gaze_inside = False
        self.update()

    # ------------------------------------------------------------ painting
    def _fit_font(self, text, max_w, max_h, start_px):
        px = start_px
        while px > 14:
            f = QFont()
            f.setFamilies(_families(UI_FONT))
            f.setBold(True)
            f.setPixelSize(px)
            r = QFontMetrics(f).boundingRect(
                0, 0, int(max_w), 10000,
                int(Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignCenter), text)
            if r.width() <= max_w and r.height() <= max_h:
                return f
            px -= 2
        f = QFont()
        f.setFamilies(_families(UI_FONT))
        f.setBold(True)
        f.setPixelSize(14)
        return f

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        w, h = self.width(), self.height()
        focused = self.is_gaze_inside and not self.is_locked
        if focused:
            border_c, border_w = QColor(BORDER_FOCUS), 4
        elif self.is_selected:
            border_c, border_w = QColor(BORDER_SELECTED), 4
        else:
            border_c, border_w = QColor(BORDER_IDLE), 2
        half = border_w / 2
        card = QRectF(half, half, w - border_w, h - border_w)
        path = QPainterPath()
        path.addRoundedRect(card, self.radius, self.radius)

        # background (+ green flash when chosen)
        bg = QColor(CONFIRM_BG if self._confirming else self.bg_color)
        p.fillPath(path, bg)

        # sweeping fill while looking
        if self.dwell_progress > 0.0 and not self.is_locked:
            p.save()
            p.setClipPath(path)
            p.fillRect(QRectF(0, 0, w * self.dwell_progress, h), QColor(31, 41, 51, 45))
            p.restore()

        p.setPen(QPen(border_c, border_w))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(path)

        # picture + word
        text = ("✓  " + self.text_label) if self._confirming else self.text_label
        pm = get_icon(self.icon_name)
        pad = max(10, int(min(w, h) * 0.06))
        inner_w, inner_h = w - 2 * pad, h - 2 * pad
        p.setPen(QColor(self.text_color))

        if pm is None:
            f = self._fit_font(text, inner_w, inner_h, self.font_px)
            p.setFont(f)
            p.drawText(QRectF(pad, pad, inner_w, inner_h),
                       int(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap), text)
        elif w > 1.8 * h:                      # wide card: picture left, word right
            side = int(inner_h * 0.85)
            gap = pad
            f = self._fit_font(text, inner_w - side - gap, inner_h, int(self.font_px * 0.8))
            p.setFont(f)
            tw = QFontMetrics(f).boundingRect(
                0, 0, int(inner_w - side - gap), 10000,
                int(Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignCenter), text).width()
            x0 = (w - (side + gap + tw)) / 2
            p.drawPixmap(QRectF(x0, (h - side) / 2, side, side), pm, QRectF(pm.rect()))
            p.drawText(QRectF(x0 + side + gap, pad, tw + 4, inner_h),
                       int(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap), text)
        else:                                   # normal card: picture above word
            text_h = inner_h * 0.30
            f = self._fit_font(text, inner_w, text_h, int(self.font_px * 0.8))
            p.setFont(f)
            side = min(inner_w, inner_h - text_h - pad * 0.5) * 0.95
            top = pad + (inner_h - text_h - side - pad * 0.5) / 2
            p.drawPixmap(QRectF((w - side) / 2, top, side, side), pm, QRectF(pm.rect()))
            p.drawText(QRectF(pad, top + side + pad * 0.5, inner_w, text_h),
                       int(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
                           | Qt.TextFlag.TextWordWrap), text)

        # progress ring (top-right corner, never covers the picture)
        if self.dwell_progress > 0.0 and not self.is_locked:
            r = min(20, h / 2 - 10)
            cx, cy = w - r - 16, r + 16
            p.setPen(QPen(QColor(RING_COLOR), 7))
            p.drawArc(QRectF(cx - r, cy - r, 2 * r, 2 * r), 90 * 16,
                      int(-self.dwell_progress * 360 * 16))
        p.end()
