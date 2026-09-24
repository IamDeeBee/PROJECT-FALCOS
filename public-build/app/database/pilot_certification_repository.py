# ============================================================
# File:         pilot_certification_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Pilot certification database operations.
#
# Description:
#       Handles:
#           - certification retrieval
#           - active pilot retrieval
#           - pilot certification creation
#           - pilot certification updates
#
# Author: Debe Okoye
# Created: 2026-08-26
# ============================================================
from app.config.constants import DB_SCHEMA, DEMO_MODE
from app.database.connection import get_connection

def get_certifications():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				ce.cert_id,
				ce.cert_name
			FROM {DB_SCHEMA}.certifications ce
			ORDER BY
				ce.cert_id
		"""
		
		cursor.execute(query)
		return cursor.fetchall()
		
	finally:
		cursor.close()
		conn.close()

def get_active_pilots():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				p.pilot_id,
				pe.person_first_name,
				pe.person_last_name,
				pe.person_primary_email
			FROM {DB_SCHEMA}.pilot p
			INNER JOIN {DB_SCHEMA}.person pe
				ON p.pilot_person_id = pe.person_id
			WHERE
				p.pilot_status_id = (
					SELECT status_id
					FROM {DB_SCHEMA}.pilot_status
					WHERE status_name = 'ACTIVE'
				)
			ORDER BY
				pe.person_last_name, pe.person_first_name
		"""
		
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def create_pilot_certification(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.pilot_certification
			(
				pilcert_cert_id,
				pilcert_pilot_id,
				pilcert_certification_number,
				pilcert_approval_status,
				pilcert_issue_date,
				pilcert_expiry_date
	
			)
			VALUES
			(
				%s,
				%s,
				%s,
				%s,
				%s,
				%s
			)
		"""
		values = (
			form_data["certification_id"],
			form_data["pilot_id"],
			form_data["certification_number"],
			form_data["approval_status"],
			form_data["issue_date"],
			form_data["expiry_date"]
		)
		cursor.execute(query, values)
		conn.commit()

	except Exception:
		conn.rollback()
		raise
	
	finally:
		cursor.close()
		conn.close()
		
def update_pilot_certification(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.pilot_certification
			SET
				pilcert_cert_id = %s,
				pilcert_pilot_id = %s,
				pilcert_certification_number = %s,
				pilcert_approval_status = %s,
				pilcert_issue_date = %s,
				pilcert_expiry_date = %s
		
			WHERE
				pilcert_id = %s 
		"""
		values = (
			form_data["certification_id"],
			form_data["pilot_id"],
			form_data["certification_number"],
			form_data["approval_status"],
			form_data["issue_date"],
			form_data["expiry_date"],
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