# Import external modules.
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets


class FailColorAnimation(QtCore.QPropertyAnimation):
    """Property animation to indicate errors.
    Displays a color transition as the color red fading out to 0 alpha.
    """
    def __init__(self, parent):
        super(FailColorAnimation, self).__init__(parent)
        effect = QtWidgets.QGraphicsColorizeEffect(parent)
        effect.setStrength(1)
        parent.setGraphicsEffect(effect)

        # Defaults.
        self.setPropertyName(b'color')
        self.setTargetObject(effect)

        self.__start_color = QtGui.QColor(255, 0, 0, 225)
        self.__end_color = QtGui.QColor(255, 0, 0, 0)
        self.__duration = 500
        self.__curve = QtCore.QEasingCurve.InQuint

        self.finished.connect(self._on_finish)

    # Public.
    def play(self, color=None, duration=None, curve=None):
        """Play the property animation.

        Args:
            color (QtCore.QColor): Override the default "red" color to
                indicate errors.
            duration (int): Override the default duration of the animation.
            curve (QtCore.QEasingCurve): Override the default easing curve
            for the animation.
        """
        if color:
            start_color = color
            end_color = QtGui.QColor(start_color)
            end_color.setAlpha(0)
        else:
            start_color = self.__start_color
            end_color = self.__end_color

        dur = self.__duration if duration is None else duration
        curve = self.__curve if curve is None else curve

        # Play animation.
        self.setStartValue(start_color)
        self.setEndValue(end_color)
        self.setEasingCurve(curve)
        self.setDuration(dur)
        self.start()

    # Slots.
    @QtCore.Slot()
    def _on_finish(self):
        """Triggered when animation is finished playing."""
        # Remove the graphic effect from the widget so that its base
        # styling isn't affected.
        self.parent().setGraphicsEffect(None)
