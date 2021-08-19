# Import built-in modules.
import enum

# Import local modules.
from Qt import QtGui


class __ColorPaletteMap(enum.Enum):
    A = (200, 0, 0)
    B = (150, 0, 0)
    C = (200, 0, 100)
    D = (150, 0, 50)
    E = (200, 50, 200)
    F = (150, 25, 150)
    G = (120, 0, 200)
    H = (95, 0, 150)
    I = (0, 40, 200)
    J = (0, 20, 150)
    K = (0, 120, 200)
    L = (0, 80, 150)
    M = (0, 200, 200)
    N = (0, 150, 150)
    O = (0, 200, 120)
    P = (0, 150, 80)
    Q = (0, 200, 0)
    R = (0, 150, 0)
    S = (120, 200, 0)
    T = (80, 150, 0)
    U = (200, 190, 0)
    V = (150, 140, 0)
    W = (180, 140, 25)
    X = (130, 90, 25)
    Y = (200, 75, 0)
    Z = (150, 50, 0)
    NUM = (50, 50, 50)
    OTHER = (50, 50, 50)


def get_mapped_color(text):
    text = text.capitalize()[0]

    if hasattr(__ColorPaletteMap, text):
        return QtGui.QColor(*getattr(__ColorPaletteMap, text).value)
    elif text.isnumeric():
        return QtGui.QColor(*getattr(__ColorPaletteMap, 'NUM').value)
    else:
        return QtGui.QColor(*getattr(__ColorPaletteMap, 'OTHER').value)


def tint_icon_color(icon, size, color):
    """Tint the icon using the provided color.

    Tint opacity determined by the alpha channel.

    Args:
        icon (QIcon): Icon to tint with the provided color.
        size (int): The icon resolution, in pixels.
        color (tuple): RGBA color values.

    Returns:
        Tinted QIcon object.
    """
    color = QtGui.QColor(*color)
    pixmap = icon.pixmap(size, size)

    painter = QtGui.QPainter(pixmap)
    painter.setCompositionMode(painter.CompositionMode_SourceAtop)
    painter.fillRect(pixmap.rect(), color)
    painter.end()

    icon.addPixmap(pixmap)

    return icon


def pastelize_color(color):
    if isinstance(color, QtGui.QColor):
        color = [color.red(), color.green(), color.blue(), color.alpha()]

    pastel_color = QtGui.QColor(*color)
    pastel_color = pastel_color.lighter(140)
    pastel_color.setHsl(
        pastel_color.hslHue(),
        150,  # Consistent saturation.
        min(max(pastel_color.lightness(), 100), 160)  # Clamp: 100-160.
    )

    return pastel_color


def desaturate(color, percent):
    if isinstance(color, QtGui.QColor):
        color = [color.red(), color.green(), color.blue(), color.alpha()]

    desaturated_color = QtGui.QColor(*color)
    desaturated_color.setHsvF(
        desaturated_color.hsvHueF(),
        max(desaturated_color.hsvSaturationF() - (percent / 100), 0),
        desaturated_color.valueF()
    )

    return desaturated_color
