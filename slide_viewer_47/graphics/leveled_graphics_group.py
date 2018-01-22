import typing

from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRectF, QRect, Qt
from PyQt5.QtGui import QPixmapCache, QColor, QBrush

from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsRectItem, QGraphicsItemGroup
import openslide


class MyGraphicsGroup(QGraphicsItemGroup):

    def __init__(self, parent: typing.Optional['QGraphicsItem'] = None) -> None:
        super().__init__(parent)
        # self.setFlag(QGraphicsItem.ItemContainsChildrenInShape, True)

    def boundingRect(self) -> QRectF:
        return QRectF()


class LeveledGraphicsGroup(QGraphicsItemGroup):
    def __init__(self, levels: typing.List[int], parent=None):
        super().__init__(parent)
        self.levels = levels
        self.level__group = {}
        for level in levels:
            # group = QGraphicsItemGroup(self)
            group = MyGraphicsGroup(self)
            group.setVisible(False)
            group.setOpacity(0.0)
            self.level__group[level] = group
        self.visible_level = None
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setAcceptHoverEvents(False)

        # self.setFlag(QGraphicsItem.ItemHasNoContents, True)
        # self.setFlag(QGraphicsItem.ItemContainsChildrenInShape, True)
        self.setFlag(QGraphicsItem.ItemClipsChildrenToShape, True)

    def boundingRect(self):
        # bounding_rect = QRectF()
        if self.visible_level:
            return self.level__group[self.visible_level].boundingRect()
        else:
            return QRectF()
        # return bounding_rect

    def add_item_to_level_group(self, level, item: QGraphicsItem):
        self.level__group[level].addToGroup(item)
        # item.setVisible(False)

    def remove_item_from_level_group(self, level, item: QGraphicsItem):
        self.level__group[level].removeFromGroup(item)

    def clear_level(self, level):
        group = self.level__group[level]
        for item in group.childItems():
            group.removeFromGroup(item)
            group.scene().removeItem(item)

    def update_visible_level(self, visible_level):
        self.visible_level = visible_level
        for level in self.levels:
            group = self.level__group[level]
            group.setVisible(level == visible_level)
            group.setOpacity(level == visible_level)