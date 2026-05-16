# 🗺 Professional Land Measurement System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-success?logo=qt)
![Google Maps API](https://img.shields.io/badge/Google_Maps-API-red?logo=googlemaps)
![SQLite](https://img.shields.io/badge/SQLite-Database-07405E?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

### 🛰️ High-Precision Geospatial Land Measurement & Mapping Platform

A modern hybrid desktop GIS-style application built with **Python + PyQt6**, powered by the **Google Maps JavaScript API**, designed for accurate land boundary measurement, geospatial area calculations, and offline client data management.

</div>

---

# 📌 Overview

The **Professional Land Measurement System** is a standalone desktop solution engineered for surveyors, land officers, property developers, real estate professionals, and GIS enthusiasts.

The application combines:

- 🗺️ Interactive Google Maps rendering
- 📐 Advanced geodesic area calculations
- 💾 Offline SQLite storage
- ⚡ Fast desktop-native performance
- 🔒 Secure API key handling

Unlike traditional web-only map tools, this system delivers a **desktop-grade experience** while leveraging the power and precision of modern geospatial web technologies.

---

# ✨ Key Features

## 🗺️ Interactive GIS Mapping Engine

- Embedded Chromium browser using `QWebEngineView`
- Real-time Google Maps rendering
- Smooth zooming, panning, and map interactions
- Hybrid desktop-web architecture

---

## ✏️ Advanced Polygon Drawing System

- Draw custom land boundaries directly on the map
- Edit and reshape polygons dynamically
- Precision coordinate capture
- Supports irregular property layouts

---

## 📐 High-Accuracy Geospatial Calculations

Powered by:

- `pyproj`
- `shapely`

The system converts raw GPS coordinates into highly accurate geodesic measurements.

### Supported Measurement Units

| Unit | Description |
|------|-------------|
| Square Meters | Standard metric land measurement |
| Acres | International land measurement |
| Perches | Common Sri Lankan land unit |

---

## 🔍 Integrated Smart Location Search

- Search cities, roads, villages, and landmarks
- Instant map navigation
- Real-time geocoding integration
- Faster property locating workflow

---

## 💾 Offline Data Persistence

Built-in SQLite database allows:

- Saving measurement history
- Managing client land records
- Offline accessibility
- Zero external database setup

---

## 🔐 Secure API Key Injection

Your Google Maps API key is:

✅ Dynamically injected at runtime  
✅ Never hardcoded into source files  
✅ Hidden using environment variables

This improves:
- Security
- Maintainability
- Production readiness

---

# 🖼️ Application Architecture

```text
┌──────────────────────────────┐
│         PyQt6 Desktop        │
│      (Main Application)      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      QWebEngineView          │
│   Embedded Chromium Engine   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Google Maps JavaScript API   │
│  Drawing + Geometry Engine   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Python Geo Processing Layer  │
│ (Shapely + PyProj)           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      SQLite Database         │
│  Offline Measurement Store   │
└──────────────────────────────┘
```

---

# 🛠️ Technology Stack

## 💻 Backend

- Python 3
- PyQt6
- SQLite3

## 🌐 Frontend

- HTML5
- CSS3
- JavaScript
- Google Maps JavaScript API

## 📐 Geospatial Processing

- Shapely
- PyProj

## 🔗 Communication Layer

- QWebChannel
- JS ↔ Python Bridge

---

# ⚙️ Prerequisites

Before running the project, ensure you have:

## ✅ Required Software

- Python 3.10 or higher
- pip package manager
- Google Cloud Platform account

---

## ✅ Enable Required Google APIs

Inside Google Cloud Console, enable:

- Maps JavaScript API
- Geocoding API

---

# 📥 Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https:/akalankapulinda/github.com//land-measurer.git
cd land-measurer
```

---

## 2️⃣ Create Virtual Environment

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

---

## 5️⃣ Run the Application

```bash
python main.py
```

---

# 📂 Project Structure

```text
land_measurer/
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignored files
├── .env                         # Environment variables
│
├── app/
│   ├── core/
│   │   ├── bridge.py            # JS ↔ Python communication bridge
│   │   ├── db_manager.py        # SQLite database operations
│   │   └── geo_engine.py        # Geospatial calculations
│   │
│   └── map_view/
│       └── map.html             # Google Maps frontend UI
│
├── data/
│   └── storage.db               # Auto-generated database
│
└── assets/
    └── screenshots/             # Project screenshots
```

---

# 🧠 How It Works

## Step 1 — Draw Land Boundary

Users outline a property using polygon drawing tools.

## Step 2 — Coordinate Collection

Google Maps captures GPS coordinates from the polygon.

## Step 3 — Geospatial Processing

Python processes coordinates using:
- Coordinate projection
- Geodesic calculations
- Polygon area computation

## Step 4 — Result Generation

The system calculates:
- Total area
- Acres
- Perches
- Coordinate data

## Step 5 — Offline Storage

Measurement data is stored locally inside SQLite.

---

# 📸 Screenshots

## Main Dashboard
<img width="1920" height="1080" alt="Screenshot (180)" src="https://github.com/user-attachments/assets/51f8cf1d-42f8-4bc4-a0f4-818b17c37d4c" />


## Polygon Drawing Interface

<img width="1920" height="1080" alt="Screenshot (182)" src="https://github.com/user-attachments/assets/5f269a93-5aea-4d83-afeb-589a80dcfcaa" />


## Measurement Results

<img width="1920" height="1080" alt="Screenshot (181)" src="https://github.com/user-attachments/assets/5d1769ca-8d94-4321-a426-3d88029e904a" />


---

# 🚀 Future Improvements

Planned features:

- 📄 PDF report exporting
- 🛰️ Satellite imagery enhancements
- 📍 GPS device integration
- ☁️ Cloud synchronization
- 📊 Land analytics dashboard
- 🌐 Multi-language support
- 📱 Mobile companion application

---

# 🔒 Security Considerations

- API keys stored securely in environment variables
- Sensitive credentials excluded via `.gitignore`
- No hardcoded secrets
- Offline-first architecture minimizes cloud exposure

---

# 🧪 Development Notes

Generate your dependency file using:

```bash
pip freeze > requirements.txt
```

---

## Steps

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this software.

---

# 👨‍💻 Author

### KKP
Full Stack Developer

- GitHub: https://github.com/akalankapulinda
- LinkedIn: https://linkedin.com/in/007akalankapulinda

### Developed with ❤️ using Python, PyQt6, and Geospatial Technologies

If you found this project useful, consider giving it a ⭐ on GitHub!

---

<div align="center">

## ⭐ Star This Repository If You Like The Project ⭐

</div>
