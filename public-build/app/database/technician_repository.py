# ============================================================
# File:         technician_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Technician database operations.
#
# Description:
#       Handles:
#           - available personnel retrieval
#           - technician retrieval
#           - company retrieval
#           - personnel detail retrieval
#           - technician creation
#           - technician updates
#
# Author: Debe Okoye
# Created: 2026-08-26
# ============================================================
from app.config.constants import DB_SCHEMA, DEMO_MODE
from app.database.connection import get_connection

def get_available_personnel():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				pe.person_id,
				pe.person_first_name,
				pe.person_last_name,
				pe.person_primary_email
			FROM {DB_SCHEMA}.person pe
			LEFT JOIN {DB_SCHEMA}.technician t
				ON pe.person_id = t.technician_person_id
			WHERE
				t.technician_person_id IS NULL
			ORDER BY
				pe.person_last_name,
				pe.person_first_name
		"""
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_all_technicians():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				pe.person_id,
				pe.person_first_name,
				pe.person_last_name,
				pe.person_primary_email
			FROM {DB_SCHEMA}.person pe
			INNER JOIN {DB_SCHEMA}.technician t
				ON pe.person_id = t.technician_person_id
			ORDER BY
				pe.person_last_name,
				pe.person_first_name
	
		"""
		
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_all_companies():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				c.company_id,
				c.company_name
			FROM {DB_SCHEMA}.company c
			ORDER BY
				c.company_id
		"""
		
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_person_details(person_id):
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				pe.person_first_name,
				pe.person_last_name,
				pe.person_primary_email
			FROM {DB_SCHEMA}.person pe
			WHERE
				pe.person_id = %s
		"""
		values = (person_id, )
		cursor.execute(query, values)

		return cursor.fetchone()

	finally:
		cursor.close()
		conn.close()

def create_technician(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.technician
			(
				technician_person_id,
				technician_company_id
			)
			VALUES
			(
				%s,
				%s
			)
		"""
		values = (
			form_data["person_id"],
			form_data["company_id"]
		)
		cursor.execute(query, values)
		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()

def update_technician(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.technician
			SET
				technician_person_id = %s,
				technician_company_id = %s
			WHERE
				technician_id = %s
		"""
		values = (
			form_data["person_id"],
			form_data["company_id"],
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

