# ============================================================
# File:         dashboard_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Dashboard database access operations.
#
#
# Description:
#       Handles:
#       - dashboard summary retrieval
#       - dashboard database operations
#
#
# Author: Debe Okoye
# Created: 2026-08-24
# ============================================================
from psycopg2.extras import RealDictCursor
from app.config.constants import DB_SCHEMA

# ============================================================
# Dashboard Summary Queries
# ============================================================
def get_alert_summary(conn):
	query = f"""
		SELECT
			pilot_pending_verification,
			certification_pending,
			certification_to_expired,
			certification_expired,
			reservation_pending_validation,
			maintenance_reported
		FROM {DB_SCHEMA}.vw_summary_alert;		
	"""

	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(query)
		return cursor.fetchone()

def get_certification_summary(conn):
	query = f"""
		SELECT
			total_certifications,
			active_pilot_certification
		FROM {DB_SCHEMA}.vw_summary_certification;		
	"""

	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(query)
		return cursor.fetchone()

def get_fleet_summary(conn):
	query = f"""
		SELECT
			total_fleet,
			operational,
			reserved,
			in_flight,
			grounded,
			decommissioned,
			maintenance
		FROM {DB_SCHEMA}.vw_summary_fleet;		
	"""

	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(query)
		return cursor.fetchone()

def get_flight_summary(conn):
	query = f"""
		SELECT
			total_flight,
			scheduled,
			progress
		FROM {DB_SCHEMA}.vw_summary_flight;		
	"""

	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(query)
		return cursor.fetchone()

def get_maintenance_summary(conn):
	query = f"""
		SELECT
			total_maintenance,
			reported,
			progress
		FROM {DB_SCHEMA}.vw_summary_maintenance;
	"""

	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(query)
		return cursor.fetchone()

def get_personnel_summary(conn):
	query = f"""
		SELECT
			total_personnel,
			active_pilots,
			total_technicians	
		FROM {DB_SCHEMA}.vw_summary_personnel;
	"""

	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(query)
		return cursor.fetchone()

