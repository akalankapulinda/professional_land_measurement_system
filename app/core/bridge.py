import json
from PyQt6.QtCore import QObject, pyqtSlot

class MapBridge(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    @pyqtSlot(str)
    def receive_coordinates(self, json_coord_data):
        """This method gets called directly from JavaScript when a polygon is complete."""
        try:
            coords = json.loads(json_coord_data)
            print(f"Received boundary data successfully with {len(coords)} vertices.")
            
            # Forward the coordinates to the main window for calculation processing
            self.main_window.process_new_land_data(coords)
            
        except Exception as e:
            print(f"Error handling coordinate payload: {e}")