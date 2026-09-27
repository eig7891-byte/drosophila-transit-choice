"""
Local Transit & FlyConnectome Database Interface
===============================================
Encapsulates all SQLite query operations for local empirical validation,
auditing, and simulation input ingestion.

Thread-safe and supports zero-dependency local querying.
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import pandas as pd

# Root path resolution
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = ROOT_DIR / "data" / "brisbane_transit.db"
DB_PATH = DEFAULT_DB_PATH

def get_connection(db_path: Optional[Union[str, Path]] = None) -> sqlite3.Connection:
    """Returns an active SQLite connection to the transit database."""
    target_path = Path(db_path) if db_path else DEFAULT_DB_PATH
    if not target_path.exists():
        raise FileNotFoundError(
            f"Database not found at '{target_path}'. Please run 'python scripts/build_database.py' first."
        )
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    return conn

class TransitDatabase:
    """High-level query interface for the local Brisbane transit database."""

    def __init__(self, db_path: Optional[Union[str, Path]] = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH

    def query_df(self, query: str, params: Optional[Union[tuple, list, dict]] = None) -> pd.DataFrame:
        """Executes a SQL query and returns results as a pandas DataFrame."""
        with get_connection(self.db_path) as conn:
            if params:
                return pd.read_sql_query(query, conn, params=params)
            return pd.read_sql_query(query, conn)

    def get_status(self) -> Dict[str, Any]:
        """Returns database status, metadata, and row counts for each table."""
        with get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
            tables = [r[0] for r in cursor.fetchall()]

            table_counts = {}
            for t in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {t}")
                table_counts[t] = cursor.fetchone()[0]

            cursor.execute("SELECT key, value, updated_at FROM db_metadata;")
            metadata = {r["key"]: {"value": r["value"], "updated_at": r["updated_at"]} for r in cursor.fetchall()}

        return {
            "db_path": str(self.db_path),
            "file_size_bytes": os.path.getsize(self.db_path) if self.db_path.exists() else 0,
            "table_counts": table_counts,
            "metadata": metadata
        }

    # -------------------------------------------------------------------------
    # 1. Patronage Queries
    # -------------------------------------------------------------------------
    def get_patronage(
        self,
        mode: Optional[str] = None,
        financial_year: Optional[str] = None,
        policy_era: Optional[str] = None
    ) -> pd.DataFrame:
        """Queries longitudinal patronage records with optional filtering."""
        sql = "SELECT * FROM patronage_records WHERE 1=1"
        params = []
        if mode:
            sql += " AND mode = ?"
            params.append(mode)
        if financial_year:
            sql += " AND financial_year = ?"
            params.append(financial_year)
        if policy_era:
            sql += " AND policy_era = ?"
            params.append(policy_era)
        sql += " ORDER BY financial_year ASC, quarter ASC, mode ASC;"
        return self.query_df(sql, params)

    def get_patronage_by_era_summary(self) -> pd.DataFrame:
        """Returns aggregate patronage statistics grouped by Policy Era and Mode."""
        sql = """
        SELECT 
            policy_era,
            mode,
            COUNT(*) as record_quarters,
            SUM(patronage) as total_patronage,
            ROUND(AVG(patronage), 0) as avg_quarterly_patronage,
            MIN(patronage) as min_quarterly_patronage,
            MAX(patronage) as max_quarterly_patronage
        FROM patronage_records
        GROUP BY policy_era, mode
        ORDER BY total_patronage DESC;
        """
        return self.query_df(sql)

    # -------------------------------------------------------------------------
    # 2. Service Reliability & On-Time Running (OTR)
    # -------------------------------------------------------------------------
    def get_service_reliability(
        self,
        mode: Optional[str] = None,
        metric_keyword: Optional[str] = None
    ) -> pd.DataFrame:
        """Queries on-time running and service delivery performance."""
        sql = "SELECT * FROM service_reliability WHERE 1=1"
        params = []
        if mode:
            sql += " AND mode = ?"
            params.append(mode)
        if metric_keyword:
            sql += " AND metric_name LIKE ?"
            params.append(f"%{metric_keyword}%")
        sql += " ORDER BY financial_year DESC, quarter DESC;"
        return self.query_df(sql, params)

    # -------------------------------------------------------------------------
    # 3. Customer Experience (CE) Ratings
    # -------------------------------------------------------------------------
    def get_customer_experience(
        self,
        metric_keyword: Optional[str] = None,
        mode: Optional[str] = None,
        min_score: Optional[float] = None
    ) -> pd.DataFrame:
        """Queries customer satisfaction scores from TransLink surveys."""
        sql = "SELECT * FROM customer_experience WHERE 1=1"
        params = []
        if metric_keyword:
            sql += " AND metric_name LIKE ?"
            params.append(f"%{metric_keyword}%")
        if mode:
            sql += " AND mode = ?"
            params.append(mode)
        if min_score is not None:
            sql += " AND score >= ?"
            params.append(min_score)
        sql += " ORDER BY financial_year DESC, quarter DESC, score DESC;"
        return self.query_df(sql, params)

    # -------------------------------------------------------------------------
    # 4. Commute Corridors
    # -------------------------------------------------------------------------
    def get_corridors(self, name_keyword: Optional[str] = None) -> pd.DataFrame:
        """Queries Brisbane commute corridor specifications."""
        sql = "SELECT * FROM commute_corridors WHERE 1=1"
        params = []
        if name_keyword:
            sql += " AND (name LIKE ? OR corridor_type LIKE ?)"
            params.extend([f"%{name_keyword}%", f"%{name_keyword}%"])
        sql += " ORDER BY distance_km ASC;"
        return self.query_df(sql, params)

    # -------------------------------------------------------------------------
    # 5. Connectome Neuron Catalog
    # -------------------------------------------------------------------------
    def get_neurons(
        self,
        transit_role: Optional[str] = None,
        primary_type: Optional[str] = None
    ) -> pd.DataFrame:
        """Queries FlyWire connectome neurons mapped to transit choices."""
        sql = "SELECT * FROM neuron_catalog WHERE 1=1"
        params = []
        if transit_role:
            sql += " AND transit_role LIKE ?"
            params.append(f"%{transit_role}%")
        if primary_type:
            sql += " AND primary_type LIKE ?"
            params.append(f"%{primary_type}%")
        sql += " ORDER BY transit_role ASC, primary_type ASC;"
        return self.query_df(sql, params)

    # -------------------------------------------------------------------------
    # 6. Model Calibration Parameters & Targets
    # -------------------------------------------------------------------------
    def get_calibration_parameters(self) -> pd.DataFrame:
        """Returns calibrated neural weights and MLE optimization metrics."""
        sql = "SELECT * FROM calibration_parameters ORDER BY id ASC;"
        return self.query_df(sql)

    def get_calibration_targets(self) -> pd.DataFrame:
        """Returns empirical targets vs uncalibrated and calibrated predictions."""
        sql = "SELECT * FROM calibration_targets ORDER BY id ASC;"
        return self.query_df(sql)

    # -------------------------------------------------------------------------
    # 7. Policy Scenarios
    # -------------------------------------------------------------------------
    def get_policy_scenarios(self) -> pd.DataFrame:
        """Returns macro policy simulation outcomes."""
        sql = "SELECT * FROM policy_scenarios ORDER BY id ASC;"
        return self.query_df(sql)

    # -------------------------------------------------------------------------
    # 8. Cross-Table Universal Search
    # -------------------------------------------------------------------------
    def search_all(self, keyword: str) -> Dict[str, pd.DataFrame]:
        """Performs a multi-table search for any keyword across all database tables."""
        kw_pattern = f"%{keyword}%"
        results = {}

        # Corridors
        corridors_df = self.query_df(
            "SELECT * FROM commute_corridors WHERE name LIKE ? OR notes LIKE ?;",
            [kw_pattern, kw_pattern]
        )
        if not corridors_df.empty:
            results["commute_corridors"] = corridors_df

        # Neurons
        neurons_df = self.query_df(
            "SELECT * FROM neuron_catalog WHERE primary_type LIKE ? OR transit_role LIKE ? OR name LIKE ? OR root_id LIKE ?;",
            [kw_pattern, kw_pattern, kw_pattern, kw_pattern]
        )
        if not neurons_df.empty:
            results["neuron_catalog"] = neurons_df

        # Patronage
        patronage_df = self.query_df(
            "SELECT * FROM patronage_records WHERE network LIKE ? OR mode LIKE ? OR financial_year LIKE ? OR policy_era LIKE ? LIMIT 50;",
            [kw_pattern, kw_pattern, kw_pattern, kw_pattern]
        )
        if not patronage_df.empty:
            results["patronage_records"] = patronage_df

        # Reliability
        rel_df = self.query_df(
            "SELECT * FROM service_reliability WHERE metric_name LIKE ? OR mode LIKE ? OR network LIKE ? LIMIT 50;",
            [kw_pattern, kw_pattern, kw_pattern]
        )
        if not rel_df.empty:
            results["service_reliability"] = rel_df

        # Customer Experience
        ce_df = self.query_df(
            "SELECT * FROM customer_experience WHERE metric_name LIKE ? OR mode LIKE ? OR network LIKE ? LIMIT 50;",
            [kw_pattern, kw_pattern, kw_pattern]
        )
        if not ce_df.empty:
            results["customer_experience"] = ce_df

        # Parameters
        param_df = self.query_df(
            "SELECT * FROM calibration_parameters WHERE parameter_name LIKE ? OR description LIKE ? OR biological_circuit LIKE ?;",
            [kw_pattern, kw_pattern, kw_pattern]
        )
        if not param_df.empty:
            results["calibration_parameters"] = param_df

        # Targets
        target_df = self.query_df(
            "SELECT * FROM calibration_targets WHERE corridor_metric LIKE ?;",
            [kw_pattern]
        )
        if not target_df.empty:
            results["calibration_targets"] = target_df

        # Policy
        policy_df = self.query_df(
            "SELECT * FROM policy_scenarios WHERE scenario_name LIKE ? OR scenario_key LIKE ?;",
            [kw_pattern, kw_pattern]
        )
        if not policy_df.empty:
            results["policy_scenarios"] = policy_df

        return results

_GLOBAL_DB: Optional[TransitDatabase] = None

def get_db(db_path: Optional[Union[str, Path]] = None) -> TransitDatabase:
    """Returns a singleton instance of TransitDatabase."""
    global _GLOBAL_DB
    if _GLOBAL_DB is None or (db_path and _GLOBAL_DB.db_path != Path(db_path)):
        _GLOBAL_DB = TransitDatabase(db_path)
    return _GLOBAL_DB
