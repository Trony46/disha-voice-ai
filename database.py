"""
database.py
-----------
Mock logistics database using SQLite.
Pre-loaded with dummy AWB (Air Waybill) tracking numbers for testing.
"""

import sqlite3
import os

DB_PATH = "logistics.db"


def init_db():
    """Create the database and seed it with dummy data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            awb_number TEXT PRIMARY KEY,
            customer_name TEXT,
            status TEXT,
            location TEXT,
            expected_delivery TEXT,
            reason TEXT
        )
    """)

    # Dummy tracking data — feel free to add more AWB numbers here
    dummy_data = [
        ("AWB001", "Ramesh Sharma",    "Delayed",    "Delhi Hub",        "2 days",        "Heavy rain causing road blockage in Delhi NCR"),
        ("AWB002", "Priya Verma",      "In Transit",  "Lucknow Facility", "Tomorrow 6 PM", "On time, shipment moving normally"),
        ("AWB003", "Suresh Gupta",     "Out for Delivery", "Your City",  "Today by 9 PM", "Your package is with the delivery agent"),
        ("AWB004", "Anita Patel",      "Stuck at Customs",  "Mumbai Airport", "3-5 days", "Documentation verification in progress"),
        ("AWB005", "Vijay Kumar",      "Delivered",   "Delivered",        "Delivered",     "Package delivered successfully on Monday"),
        ("AWB123", "Angry Uncle Ji",   "Delayed",     "Ghaziabad Depot",  "3 days",        "Vehicle breakdown near NH-9; rerouting in progress"),
        ("AWB999", "Test User",        "Lost",        "Unknown",          "Unknown",       "We are investigating the shipment location"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO shipments
        (awb_number, customer_name, status, location, expected_delivery, reason)
        VALUES (?, ?, ?, ?, ?, ?)
    """, dummy_data)

    conn.commit()
    conn.close()
    print(f"[DB] Database initialized at '{DB_PATH}' with {len(dummy_data)} records.")


def get_shipment_status(awb_number: str) -> dict | None:
    """
    Query shipment info by AWB number.
    Returns a dict with shipment details, or None if not found.
    """
    awb_number = awb_number.strip().upper()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT awb_number, customer_name, status, location, expected_delivery, reason
        FROM shipments
        WHERE UPPER(awb_number) = ?
    """, (awb_number,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "awb_number": row[0],
            "customer_name": row[1],
            "status": row[2],
            "location": row[3],
            "expected_delivery": row[4],
            "reason": row[5],
        }
    return None


# Auto-initialize when this module is imported
init_db()
