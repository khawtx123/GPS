import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QMouseEvent
from PyQt5.QtCore import QTimer, Qt
from PyQt5.uic import loadUi

# Define some constants
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 463
PLANTATION_MAP = "C:\\Users\\cyx02\\Downloads\\Documents\\IDP\\plantationmap.jpg"  # Replace with your actual map image
NUM_TREES = 100
TREES_PER_COLUMN = 20
HARVEST_TIME = 5000  # 5 seconds

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.map_label = QLabel()
        self.coord_label = QLabel("Coordinates: (0, 0)")
        self.message_text = QTextEdit()
        self.message_text.setReadOnly(True)
        self.status_label = QLabel()
        self.initUI()

        # Initialize tree coordinates and harvested status
        self.fruits_harvested = 0
        self.tree_coords = self.arrange_trees_in_columns()
        self.harvested_trees = []
        print(f"Initialized {NUM_TREES} tree coordinates.")

        # Initialize machine coordinates and timer
        self.machine_coord = self.tree_coords[0]
        self.current_column_index = 0
        self.current_tree_index = 0
        self.column_direction = 1  # 1 for top to bottom, -1 for bottom to top

        # Create a pixmap and painter for drawing
        self.pixmap = QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.pixmap.fill(Qt.white)
        self.painter = QPainter(self.pixmap)

        # Draw the initial map image
        map_image = QPixmap(PLANTATION_MAP)
        self.painter.drawPixmap(0, 0, map_image)

        self.timer = QTimer()
        self.timer.timeout.connect(self.harvestTree)
        self.timer.start(HARVEST_TIME)
        print("Timer started.")

    def initUI(self):
        self.setWindowTitle("Plantation Dashboard")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        loadUi('palmoildashboard.ui', self)
        self.map_label.setMouseTracking(True)
        self.map_label.mouseMoveEvent = self.mouseMoveEvent

        # Create a label to display the map and tree/machine status
        self.map_label = QLabel()
        pixmap = QPixmap(PLANTATION_MAP)
        self.map_label.setPixmap(pixmap)
        self.map_label.setAlignment(Qt.AlignLeft)
        self.map_label.setMouseTracking(True)  # Enable mouse tracking for the label
        self.map_label.mouseMoveEvent = self.mouseMoveEvent  # Override the mouseMoveEvent method

        # Create a label to display the coordinates
        self.coord_label = QLabel("Coordinates: (0, 0)")
        self.coord_label.setAlignment(Qt.AlignHCenter)

        # Create a layout to hold the map label, coordinate label, and message text
        container = QWidget()
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.map_label)
        top_layout.addWidget(self.coord_label)
        layout.addLayout(top_layout)
        layout.addWidget(self.message_text)
        layout.addWidget(self.status_label)
        container.setLayout(layout)

        self.setCentralWidget(container)

    def displayMessage(self, message):
        self.message_text.append(message)

    def mouseMoveEvent(self, event: QMouseEvent):
        # Get the mouse coordinates relative to the map label
        mouse_x = event.x()
        mouse_y = event.y()

        # Find the closest tree coordinate
        min_distance = float('inf')
        nearest_tree_coord = None
        for tree_coord in self.tree_coords:
            distance = ((tree_coord[0] - mouse_x) ** 2 + (tree_coord[1] - mouse_y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_tree_coord = tree_coord

        # Update the coordinates label with the nearest tree coordinate
        if nearest_tree_coord:
            self.coord_label.setText(f"Coordinates: ({nearest_tree_coord[0]}, {nearest_tree_coord[1]})")
        else:
            self.coord_label.setText("No tree found.")

    def arrange_trees_in_columns(self):
        tree_coords = []
        num_columns = NUM_TREES // TREES_PER_COLUMN + (NUM_TREES % TREES_PER_COLUMN > 0)
        column_width = (WINDOW_WIDTH - 100) // num_columns
        tree_spacing = (WINDOW_HEIGHT - 100) // (TREES_PER_COLUMN + 1)

        for col in range(num_columns):
            x = 50 + col * column_width
            for row in range(TREES_PER_COLUMN):
                if len(tree_coords) == NUM_TREES:
                    break
                y = 50 + (row + 1) * tree_spacing
                tree_coords.append((x, y))

        return tree_coords

    def harvestTree(self):
        # Simulate harvesting a tree and moving to the next one
        self.harvested_trees.append(self.machine_coord)

        # Move to the next tree in the current column
        self.current_tree_index += self.column_direction

        # Check if we need to move to the next column
        if self.current_tree_index < 0 or self.current_tree_index >= TREES_PER_COLUMN:
            self.current_column_index += 1
            self.column_direction *= -1
            self.current_tree_index = (self.current_tree_index + self.column_direction) % TREES_PER_COLUMN

        # Calculate the index of the next tree in the tree_coords list
        next_tree_index = self.current_column_index * TREES_PER_COLUMN + self.current_tree_index

        self.machine_coord = self.tree_coords[next_tree_index]

        self.fruits_harvested += 1
        self.status_label.setText(f"Machine Location: {self.machine_coord}\nFruits Harvested: {self.fruits_harvested}")

        self.displayMessage(f"Harvested tree at {self.machine_coord}. Moving to next tree.")
        self.updateMapDisplay()

    def updateMapDisplay(self):
        # Clear the pixmap
        self.pixmap.fill(Qt.white)

        # Draw the map image
        map_image = QPixmap(PLANTATION_MAP)
        self.painter.drawPixmap(0, 0, map_image)

        # Draw harvested trees as filled red circles
        brush = QBrush(Qt.red)
        self.painter.setBrush(brush)
        pen = QPen(Qt.red)
        self.painter.setPen(pen)
        for coord in self.harvested_trees:
            self.painter.drawEllipse(coord[0] - 4, coord[1] - 4, 8, 8)

        # Draw harvested tree connections as green lines
        pen = QPen(Qt.green, 4)  # Wider green lines
        self.painter.setPen(pen)
        brush = Qt.NoBrush  # Reset the brush to enable drawing lines
        self.painter.setBrush(brush)
        for i in range(len(self.harvested_trees) - 1):
            self.painter.drawLine(self.harvested_trees[i][0], self.harvested_trees[i][1],
                                  self.harvested_trees[i + 1][0], self.harvested_trees[i + 1][1])

        # Draw the machine as a filled blue circle
        brush = QBrush(Qt.blue)
        self.painter.setBrush(brush)
        pen = QPen(Qt.blue)
        self.painter.setPen(pen)
        self.painter.drawEllipse(self.machine_coord[0] - 6, self.machine_coord[1] - 6, 12, 12)

        # Set the new pixmap as the label's pixmap
        self.map_label.setPixmap(self.pixmap)
        self.displayMessage("Map display updated.")

        # Update the status label
        self.status_label.setText(f"Machine Location: {self.machine_coord}\nFruits Harvested: {self.fruits_harvested}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())


