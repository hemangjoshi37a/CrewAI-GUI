# CustomGraphicsView.py

from PySide6.QtWidgets import QGraphicsView, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPointF, QElapsedTimer
from PySide6.QtGui import QPixmap, QPainter
from Node import Node
from NodeData import NodeData
class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, main_window):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.NoDrag)
        self._dragging = False
        self._last_mouse_pos = QPointF()
        self.main_window = main_window  # Reference to the MainWindow
        self.timer = QElapsedTimer()  # Initialize the timer

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._dragging = True
            self._last_mouse_pos = event.pos()
            self.timer.start()  # Start the timer
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta = event.pos() - self._last_mouse_pos
            self._last_mouse_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self._dragging:
            self._dragging = False
            elapsed_time = self.timer.elapsed()  # Get the elapsed time
            print(f"Elapsed time: {elapsed_time} ms")  # Print the elapsed time
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def add_node(self, position):
        unique_id = f"uniq_id_{self.scene().node_counter}"
        node_data = NodeData(name="Node", uniq_id=unique_id)
        node = Node(node_data)
        self.scene().addItem(node)
        node.setPos(position)  # Set the node position to the right-click position
        self.scene().node_counter += 1  # Increment the counter
        self.update_map_view()

    def update_map_view(self):
        rect = self.scene().sceneRect()
        pixmap = QPixmap(int(rect.width()), int(rect.height()))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.scene().render(painter)
        painter.end()
        self.main_window.map_view.update_map(pixmap)  # Update the map view in the MainWindow

    def contextMenuEvent(self, event):
        self.right_click_position = self.mapToScene(event.pos())
        context_menu = QMenu(self)
        add_node_action = QAction("Add Node", self)
        add_node_action.triggered.connect(lambda: self.add_node(self.right_click_position))
        context_menu.addAction(add_node_action)
        context_menu.exec(event.globalPos())
