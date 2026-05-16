import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QWidget, 
                             QTextEdit, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QUrl
from dotenv import load_dotenv
load_dotenv() # Loads the hidden .env variables into memory
from app.core.db_manager import init_db
from app.core.bridge import MapBridge
from app.core.geo_engine import calculate_land_metrics

from app.core.db_manager import init_db, save_measurement_to_db, get_all_measurements, delete_measurement
class LandMeasurerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Land Measurement System")
        self.setGeometry(100, 100, 1300, 850)
        self.current_metrics = None
        self.current_coords = None
        # Core UI Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left Panel: Data Readout & Metrics
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(self.sidebar)
        
        sidebar_layout.addWidget(QLabel("<b>Measurement Metrics:</b>"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        sidebar_layout.addWidget(self.log_output)
        # ... existing sidebar layout code ...
        
        # --- NEW UI: Save Controls ---
        sidebar_layout.addWidget(QLabel("<b>Save Measurement:</b>"))
        
        self.plot_name_input = QLineEdit()
        self.plot_name_input.setPlaceholderText("Enter Land Name (e.g., Smith Farm)")
        sidebar_layout.addWidget(self.plot_name_input)
        
        self.save_btn = QPushButton("➜] Save to Database")
        self.save_btn.setStyleSheet("background-color: #2980b9; color: white; padding: 8px; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_data) # Connects button click to function
        sidebar_layout.addWidget(self.save_btn)
        # -----------------------------
        self.history_btn = QPushButton("◴ View Saved History")
        self.history_btn.setStyleSheet("background-color: #2c3e50; color: white; padding: 8px; margin-top: 10px;")
        self.history_btn.clicked.connect(self.open_history)
        sidebar_layout.addWidget(self.history_btn)
        main_layout.addWidget(self.sidebar)

        # Right Panel: Interactive Map Engine
        self.browser = QWebEngineView()
        
        # Apply strict policy overrides to bypass local file restrictions
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        
        main_layout.addWidget(self.browser, stretch=1)
        
        # Establish WebChannel Communication Bridge
        self.channel = QWebChannel()
        self.bridge = MapBridge(self)
        self.channel.registerObject("pyBridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)
        
        # MEMORY INJECTION FIX: Read HTML file as text and inject it straight to memory
        # MEMORY INJECTION FIX: Read HTML file and inject API key dynamically
        html_path = os.path.abspath(os.path.join("app", "map_view", "map.html"))
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                
            # --- API SECRECY FIX ---
            api_key = os.getenv("GOOGLE_MAPS_API_KEY")
            if not api_key:
                print("WARNING: GOOGLE_MAPS_API_KEY not found in .env file!")
                api_key = "MISSING_KEY"
                
            # Inject the secure key into the HTML template right before rendering
            html_content = html_content.replace("{{GOOGLE_MAPS_API_KEY}}", api_key)
            # -----------------------

            self.browser.setHtml(html_content, QUrl("http://localhost"))
        else:
            self.log_output.setText(f"ERROR: Could not find map.html at {html_path}")

    def process_new_land_data(self, coordinates):
        """Callback handled when map bridge captures coordinates."""
        self.log_output.append("<hr><b>--- New Land Plot Measured ---</b>")
        
        metrics = calculate_land_metrics(coordinates)
        
        if metrics.get("status") == "success":
            # Store in memory for the Save button
            self.current_coords = coordinates
            self.current_metrics = metrics
            
            self.log_output.append("<br><b>⌗ Area Results:</b>")
            self.log_output.append(f"• <b>Square Meters:</b> {metrics['area_sqm']:,.2f} m²")
            self.log_output.append(f"• <b>Acres:</b> {metrics['acres']:,.4f} acres")
            self.log_output.append(f"• <b>Perches:</b> {metrics['perches']:,.2f} perches")
        else:
            self.log_output.append(f"<font color='red'>Error: {metrics.get('error')}</font>")


    def save_data(self):
        """Triggered when the Save button is clicked."""
        land_name = self.plot_name_input.text().strip()
        
        # Validation checks
        if not land_name:
            QMessageBox.warning(self, "Input Error", "Please enter a name for this land plot.")
            return
        if not self.current_metrics or not self.current_coords:
            QMessageBox.warning(self, "No Data", "Please draw a land boundary on the map first.")
            return
            
        # Execute Database Save
        success = save_measurement_to_db(
            land_name=land_name,
            area_sqm=self.current_metrics['area_sqm'],
            perimeter_m=self.current_metrics['perimeter_m'],
            raw_coords=self.current_coords
        )
        
        if success:
            QMessageBox.information(self, "Success", f"'{land_name}' saved successfully!")
            self.plot_name_input.clear() # Clear the input box for the next plot
        else:
      
            QMessageBox.critical(self, "Database Error", "Failed to save the measurement.")

    def open_history(self):
        """Opens the History Dialog window."""
        dialog = HistoryDialog(self)
        dialog.exec()

        
class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Saved Land Measurements")
        self.setGeometry(200, 200, 700, 400)
        
        layout = QVBoxLayout(self)
        
        # 1. Create the Data Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Land Name", "Area (m²)", "Perimeter (m)", "Date Saved"])
        
        # Make the table look professional (stretch columns to fit)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Stretch Name column
        
        layout.addWidget(self.table)
        
        # 2. Add a Delete Button
        self.delete_btn = QPushButton("🗑 Delete Selected Plot")
        self.delete_btn.setStyleSheet("background-color: #c0392b; color: white; padding: 8px;")
        self.delete_btn.clicked.connect(self.delete_selected)
        layout.addWidget(self.delete_btn)
        
        # Load the data into the table
        self.load_data()

    def load_data(self):
        """Fetches data from SQLite and populates the table."""
        self.table.setRowCount(0) # Clear existing rows
        records = get_all_measurements()
        
        for row_idx, row_data in enumerate(records):
            self.table.insertRow(row_idx)
            for col_idx, cell_data in enumerate(row_data):
                # Format numbers for better readability
                if isinstance(cell_data, float):
                    display_text = f"{cell_data:,.2f}"
                else:
                    display_text = str(cell_data)
                    
                item = QTableWidgetItem(display_text)
                self.table.setItem(row_idx, col_idx, item)

    def delete_selected(self):
        """Deletes the highlighted row from the database."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")
            return
            
        # Get the ID from the hidden first column (Column 0)
        measurement_id = self.table.item(selected_row, 0).text()
        land_name = self.table.item(selected_row, 1).text()
        
        # Confirm deletion
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                       f"Are you sure you want to delete '{land_name}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                                       
        if confirm == QMessageBox.StandardButton.Yes:
            if delete_measurement(measurement_id):
                self.load_data() # Refresh the table
def main():
    init_db()
    
    # Advanced Chromium engine bypass arguments
    sys.argv.append("--disable-web-security")
    sys.argv.append("--allow-running-insecure-content")
    sys.argv.append("--disable-features=NetworkServiceSandbox") # Explicit network sandbox bypass
    
    app = QApplication(sys.argv)
    window = LandMeasurerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()