# ✈️ SkyWing - Global Aviation Operations Suite

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter%20Modern%20UI-38BDF8?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![Database](https://img.shields.io/badge/Database-SQLite3-00B4D8?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Theme](https://img.shields.io/badge/Theme-Obsidian%20%26%20Electric%20Sky-0B132B?style=for-the-badge)]()

An enterprise-grade desktop software built with **Python**, **Tkinter**, and **SQLite**. Designed with a modern dark-mode aviation console UI, seamless single-window sidebar navigation, real-time live flight boards with search filtering, administrative controls, dynamic ticket estimators, and trigonometric promotional reward wheels.

---

## 🎨 Modern Obsidian & Electric Sky Theme
- **Deep Aviation Obsidian (`#0B132B`)**: Sleek, immersive backdrop.
- **Card Surfaces (`#1C2541` / `#243256`)**: Layered elevation with subtle `#3A506B` strokes.
- **Electric Cyan (`#48CAE4`)**: High-visibility active tabs, badges, and primary accents.
- **Status Indicators**: Emerald (`#10B981`) for on-time flights, Amber (`#F59E0B`) for deals, Rose (`#EF4444`) for deletions.

---

## 🚀 Key Features

### 1. 🖥️ Modern Single-Window Sidebar Console
- No more clunky, floating popups! The entire application runs inside an organized desktop dashboard with an interactive sidebar (similar to Slack/Discord/Spotify).
- Instant tab-switching with active pill indicators and user session persistence.

### 2. 🛫 Live Flight Board & Admin Controls
- **Real-Time Schedule Table**: Clean custom `ttk.Treeview` with status badges (`ON TIME`, `SCHEDULED`, `BOARDING`).
- **Instant Search Bar**: Filter flights dynamically by destination, flight number, or date as you type.
- **Integrated Admin Controls**:
  - Secure PIN authentication (`123456789`).
  - Inline flight creation form.
  - Delete selected flight with confirmation dialogs.

### 3. 🎟 Fare & Ticket Price Estimator
- Dynamic dual-card calculator comparing destinations and cabin classes (`Economy`, `Business`, `First Class VIP`).
- Dual currency display (EGP & approximate USD conversion).
- Baggage allowance and amenities breakdown.

### 4. 🎡 Promotional Wheel of Fortune
- Canvas-based animation using trigonometry physics (`sin`, `cos`) with smooth deceleration steps.
- Instant voucher code generation for discounts up to 50% off (`SKYWING-XXXX`).

---

## 🏗️ Project Structure

```text
├── database.py       # SQLite database manager (Schema, Migrations & CRUD operations)
├── main.py           # Modern Aviation Suite App & All UI Views
├── arline.py         # Backward-compatibility runner
├── run.ps1           # Quick-launch PowerShell script
├── requirements.txt  # Dependencies guide
├── .gitignore        # Clean Git ignore file
└── README.md         # Documentation
```

---

## 💻 Getting Started

### Prerequisites
- Python 3.8+ installed (uses standard library modules: `tkinter`, `sqlite3`, `math`, `random`).

### Run Application
```bash
python main.py
```
*(On Windows, you can also launch via `./run.ps1`)*

---

## 🔑 Admin Security PIN
- **Admin PIN**: `123456789`
