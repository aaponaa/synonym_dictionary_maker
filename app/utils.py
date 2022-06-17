from typing import TypeVar

from PyQt5.QtWidgets import *

T = TypeVar("T")


def label(text: str, width: int = None, height: int = None) -> QLabel:
    return apply_size(QLabel(text), width, height)


def scroll_area(layout: QLayout, width: int = None, height: int = None) -> QScrollArea:
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    w1 = QWidget()
    scroll_area.setWidget(w1)
    w1.setLayout(layout)
    return apply_size(scroll_area, width, height)


def apply_size(widget: T, width: int = None, height: int = None) -> T:
    if width is not None:
        widget.setFixedWidth(width)
    if height is not None:
        widget.setFixedHeight(height)
    return widget


def horizontal_layout(*widgets: [(QWidget, int)]) -> QHBoxLayout:
    return layout(QHBoxLayout(), widgets)


def vertical_layout(*widgets: [(QWidget, int)]) -> QVBoxLayout:
    return layout(QVBoxLayout(), widgets)


def layout(l: QLayout, widgets: [(QWidget, int)]) -> QLayout:
    for (widget, stretch) in widgets:
        l.addWidget(widget, stretch=stretch)
    return l
