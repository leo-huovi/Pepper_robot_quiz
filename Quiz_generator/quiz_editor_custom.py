#!/usr/bin/env python3
"""
Pepper Robot Quiz Editor
Custom widgets for the editor UI
"""

from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap

class DraggableListWidget(QListWidget):
    """Custom list widget with drag and drop functionality"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)
        
    def startDrag(self, supportedActions):
        """Start a drag operation when item is clicked and moved"""
        item = self.currentItem()
        if not item:
            return
            
        mimeData = QMimeData()
        mimeData.setText(item.text())
        
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        
        # Create a visual representation of the dragged item
        pixmap = QPixmap(self.viewport().size())
        pixmap.fill(Qt.transparent)
        
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(self.cursor().pos()))
        
        # Execute the drag operation
        drag.exec_(supportedActions)
