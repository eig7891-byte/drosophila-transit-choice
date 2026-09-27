"""
Data Layer Package: Local Empirical Database & Storage
=====================================================
Provides clean programmatic access to the local SQLite database
(data/brisbane_transit.db) containing TransLink empirical records,
FlyWire connectome metadata, and model calibration metrics.
"""

from .database import (
    TransitDatabase,
    get_db,
    get_connection,
    DB_PATH
)

__all__ = [
    "TransitDatabase",
    "get_db",
    "get_connection",
    "DB_PATH"
]
