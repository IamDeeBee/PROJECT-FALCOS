# ============================================================
# File:         pilot_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Pilot database operations.
#
# Description:
#       Handles:
#           - available personnel retrieval
#           - pilot retrieval
#           - personnel detail retrieval
#           - pilot status retrieval
#           - pilot creation
#           - pilot updates
#
# Author: Debe Okoye
# Created: 2026-08-26
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA, DEMO_MODE

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
			LEFT JOIN {DB_SCHEMA}.pilot p
				ON pe.person_id = p.pilot_person_id
			WHERE
				p.pilot_person_id IS NULL
			ORDER BY
				pe.person_last_name,
				pe.person_first_name
		"""
		
		cursor.execute(query)

		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_all_pilots():
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
			INNER JOIN {DB_SCHEMA}.pilot p
				ON pe.person_id = p.pilot_person_id
	
			ORDER BY
				pe.person_last_name,
				pe.person_first_name
	
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

def get_pilot_statuses():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				status_id,
				status_name
			FROM {DB_SCHEMA}.pilot_status
			ORDER BY
				status_id
		"""
		cursor.execute(query)

		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def create_pilot(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				INSERT INTO {DB_SCHEMA}.pilot
				(
					pilot_person_id,
					pilot_secondary_email,
					pilot_status_id,
					pilot_flight_hours
				)
				VALUES
				(
					%s,
					%s,
					%s,
					%s
				)
			"""
		values = (
			form_data["person_id"],
			form_data["secondary_email"],
			form_data["status_id"],
			form_data["flight_hours"]
		)
		cursor.execute(query, values)

		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()

def update_pilot(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.pilot
			SET
				pilot_person_id = %s,
				pilot_secondary_email = %s,
				pilot_status_id = %s
			WHERE
				pilot_id = %s
		"""
		values = (
			form_data["person_id"],
			form_data["secondary_email"],
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
