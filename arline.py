"""
SkyWing Modern Aviation Suite
Legacy Entry Point - Forwards to main.py
"""
from main import ModernAirlineApp

if __name__ == "__main__":
    app = ModernAirlineApp()
    app.mainloop()
