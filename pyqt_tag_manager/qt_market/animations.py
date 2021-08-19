# Import external modules.
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets


class FailColorAnimation(QtCore.QPropertyAnimation):
    def __init__(self, parent):
        super(FailColorAnimation, self).__init__(parent)
        effect = QtWidgets.QGraphicsColorizeEffect(parent)
        effect.setStrength(1)
        parent.setGraphicsEffect(effect)

        # Defaults.
        self.setPropertyName(b'color')
        self.setTargetObject(effect)

        self.__start_color = QtGui.QColor(255, 0, 0, 150)
        self.__end_color = QtGui.QColor(255, 0, 0, 0)
        self.__duration = 500
        self.__curve = QtCore.QEasingCurve.InQuint

        self.finished.connect(self._on_finish)

    def play(self, color=None, duration=None, curve=None):
        if color:
            start_color = color
            end_color = QtGui.QColor(start_color)
            end_color.setAlpha(0)
        else:
            start_color = self.__start_color
            end_color = self.__end_color

        dur = duration if duration is not None else self.__duration
        curve = curve if curve is not None else self.__curve
        dur = self.__duration if duration is None else duration
        curve = self.__curve if curve is None else curve

        # Play animation.
        self.setStartValue(start_color)
        self.setEndValue(end_color)
        self.setEasingCurve(curve)
        self.setDuration(dur)
        self.start()

    @QtCore.Slot()
    def _on_finish(self):
        self.parent().setGraphicsEffect(None)
