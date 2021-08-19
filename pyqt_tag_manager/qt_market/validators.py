from Qt import QtCore
from Qt import QtGui


def only_numbers(limit=None):
    regex = '[0-9]'

    l_regex = '+' if limit is None else '{{0,{len}}}'.format(len=limit)
    regex = regex + l_regex

    return QtGui.QRegExpValidator(QtCore.QRegExp(regex))


def only_letters(limit=None):
    regex = '[a-zA-Z]'

    l_regex = '+' if limit is None else '{{0,{len}}}'.format(len=limit)
    regex = regex + l_regex

    return QtGui.QRegExpValidator(QtCore.QRegExp(regex))


def no_special_characters(limit=None, allow_chars=None):
    if allow_chars is None:
        allow_chars = []

    regex = '[0-9a-zA-Z{extra}]'.format(extra=''.join(allow_chars))

    l_regex = '+' if limit is None else '{{0,{len}}}'.format(len=limit)
    regex = regex + l_regex

    return QtGui.QRegExpValidator(QtCore.QRegExp(regex))
