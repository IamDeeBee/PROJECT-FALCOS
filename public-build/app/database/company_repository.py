# ============================================================
# File:         company_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Company database operations.
#
# Description:
#       Handles:
#           - company status retrieval
#           - company creation
#           - company updates
#
# Author: Debe Okoye
# Created: 2026-08-25
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA, DEMO_MODE

def get_company_statuses():
	if DEMO_MODE:
		return []

	try:
		conn = get_connection()
		cursor = conn.cursor()

		query = f"""
			SELECT
				status_id,
				status_name
			FROM {DB_SCHEMA}.company_status
			ORDER BY
				status_id
		"""

		cursor.execute(query)

		rows = cursor.fetchall()

		return rows

	finally:
		cursor.close()
		conn.close()

def create_company(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()


	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.company
			(
				company_name,
				company_status_id
			)
			VALUES
			(
				%s,
				%s
			)
		"""
		values = (
			form_data["name"], 
			form_data["status_id"]
		)
		cursor.execute(query, values)

		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()
		

def update_company(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.company
			SET
				company_name = %s,
				company_status_id = %s
			WHERE
				company_id = %s
		"""
		values = (
			form_data["name"],
			form_data["status_id"],
			record_id
		)
		cursor.execute(query, values)
		conn.commit()
	
	except Exception:
			conn.rollback()
			raise
	
	finally:
		cursor.close()
		conn.close()