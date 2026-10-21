import sqlite3
import os

DB_NAME = "airline.db"

class DatabaseManager:
    """Manages SQLite database operations for users and flight records."""

    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._init_db()
        self._migrate_legacy_data()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            # Flights table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    destination TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    flight_number TEXT NOT NULL
                )
            """)
            conn.commit()

    def _migrate_legacy_data(self):
        """Migrate legacy records from old flights.db and user_data.db if available."""
        # Migrate users
        if os.path.exists("user_data.db"):
            try:
                with sqlite3.connect("user_data.db") as old_conn, self._get_connection() as conn:
                    old_users = old_conn.execute("SELECT id, name, password FROM users").fetchall()
                    conn.executemany("INSERT OR IGNORE INTO users (id, name, password) VALUES (?, ?, ?)", old_users)
                    conn.commit()
            except Exception:
                pass

        # Migrate flights
        if os.path.exists("flights.db"):
            try:
                with sqlite3.connect("flights.db") as old_conn, self._get_connection() as conn:
                    # Check if flights table is empty
                    count = conn.execute("SELECT COUNT(*) FROM flights").fetchone()[0]
                    if count == 0:
                        old_flights = old_conn.execute(
                            "SELECT destination, date, time, flight_number FROM trips"
                        ).fetchall()
                        conn.executemany(
                            "INSERT INTO flights (destination, date, time, flight_number) VALUES (?, ?, ?, ?)",
                            old_flights
                        )
                        conn.commit()
            except Exception:
                pass

        # If flights still empty, seed with nice initial flight entries
        with self._get_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM flights").fetchone()[0]
            if count == 0:
                sample_flights = [
                    ("Cairo (CAI)", "2026-11-01", "08:30 AM", "MS-777"),
                    ("Paris (CDG)", "2026-11-02", "11:15 AM", "AF-1245"),
                    ("London (LHR)", "2026-11-05", "02:45 PM", "BA-5148"),
                    ("New York (JFK)", "2026-11-10", "09:00 PM", "AA-9080"),
                    ("Rome (FCO)", "2026-11-12", "04:20 PM", "AZ-3301"),
                    ("Riyadh (RUH)", "2026-11-15", "01:00 AM", "SV-202"),
                    ("Dubai (DXB)", "2026-11-18", "06:10 PM", "EK-925")
                ]
                conn.executemany(
                    "INSERT INTO flights (destination, date, time, flight_number) VALUES (?, ?, ?, ?)",
                    sample_flights
                )
                conn.commit()

    def add_user(self, user_id: int, name: str, password: str) -> bool:
        """Register a new user. Returns True on success, False if ID exists."""
        try:
            with self._get_connection() as conn:
                conn.execute("INSERT INTO users (id, name, password) VALUES (?, ?, ?)", (user_id, name, password))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, user_id: int, password: str):
        """Authenticate user by id and password. Returns username or None."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM users WHERE id = ? AND password = ?", (user_id, password))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_all_flights(self):
        """Fetch all flights ordered by date and time."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, destination, date, time, flight_number FROM flights ORDER BY id DESC")
            return cursor.fetchall()

    def add_flight(self, destination: str, date: str, time: str, flight_number: str) -> bool:
        """Add a new flight record."""
        if not all([destination.strip(), date.strip(), time.strip(), flight_number.strip()]):
            return False
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO flights (destination, date, time, flight_number) VALUES (?, ?, ?, ?)",
                (destination.strip(), date.strip(), time.strip(), flight_number.strip())
            )
            conn.commit()
            return True

    def delete_flight(self, flight_id: int) -> bool:
        """Delete a flight record by ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM flights WHERE id = ?", (flight_id,))
            conn.commit()
            return cursor.rowcount > 0
