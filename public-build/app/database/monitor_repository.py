# ============================================================
# File:         monitor_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Database operations for the monitor system.
#
# Description:
#       Handles:
#       - monitor table data retrieval
#
# Author: Debe Okoye
# Created: 2026-08-24
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA, DEMO_MODE

def get_monitor_data(db_view:str):
	if DEMO_MODE:
		return [], []
	
	conn = get_connection()
	cursor = conn.cursor()
	query = f"SELECT * FROM {DB_SCHEMA}.{db_view}"
	
	cursor.execute(query)

	rows = cursor.fetchall()
	column_names = [desc[0] for desc in cursor.description]

	cursor.close()
	conn.close()

	return rows, column_names