# ============================================================
# File:         maintenance_log_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Maintenance log database operations.
#
# Description:
#       Handles:
#           - maintenance order retrieval
#           - maintenance detail retrieval
#           - maintenance status retrieval
#           - technician retrieval
#           - maintenance log creation
#           - maintenance log updates
#
# Author: Debe Okoye
# Created: 2026-08-25
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA, DEMO_MODE

def get_reported_maintenance_orders():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query =  f"""
			SELECT
				ml.maint_id,
				fa.asset_nickname,
				ml.maint_type,
				ml.maint_reported_date
			FROM {DB_SCHEMA}.maintenance_logs ml
			INNER JOIN {DB_SCHEMA}.fleet_asset fa
				ON ml.maint_asset_id = fa.asset_id
			WHERE
				ml.maint_status_id =
				(
					SELECT status_id
					FROM {DB_SCHEMA}.maintenance_logs_status
					WHERE status_name = 'REPORTED'
				)
			ORDER BY
				ml.maint_reported_date DESC,
				fa.asset_nickname
		"""
		cursor.execute(query)

		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()
def get_all_maintenance_orders():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query =  f"""
			SELECT
				ml.maint_id,
				fa.asset_nickname,
				ml.maint_type,
				ml.maint_reported_date
			FROM {DB_SCHEMA}.maintenance_logs ml
			INNER JOIN {DB_SCHEMA}.fleet_asset fa
				ON ml.maint_asset_id = fa.asset_id
			ORDER BY
				ml.maint_reported_date DESC,
				fa.asset_nickname
		"""
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_maintenance_order_details(maint_id):
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				fa.asset_nickname,
				ml.maint_type,
				CASE
					WHEN ml.maint_reported_by_person_id IS NOT NULL
						THEN CONCAT(pe.person_first_name, ' ', pe.person_last_name)
					ELSE ml.maint_reported_by_external_name
				END,
				ml.maint_reason,
				ml.maint_status_id
			FROM {DB_SCHEMA}.maintenance_logs ml
			INNER JOIN {DB_SCHEMA}.fleet_asset fa
				ON ml.maint_asset_id = fa.asset_id
			LEFT JOIN {DB_SCHEMA}.person pe
				ON ml.maint_reported_by_person_id = pe.person_id
			WHERE
				ml.maint_id = %s
		"""
	
		cursor.execute(query, (maint_id,))
		
		return cursor.fetchone()

	finally:
		cursor.close()
		conn.close()

def get_maintenance_statuses():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				status_id,
				status_name
			FROM {DB_SCHEMA}.maintenance_logs_status
			ORDER BY
				status_id
		"""
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_technicians():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				SELECT
					t.technician_id,
					pe.person_first_name,
					pe.person_last_name,
					pe.person_primary_email
				FROM {DB_SCHEMA}.technician t
				INNER JOIN {DB_SCHEMA}.person pe
					ON t.technician_person_id = pe.person_id
				ORDER BY
					pe.person_last_name,
					pe.person_first_name;
			"""
		
		cursor.execute(query)
		
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def create_maintenance_log(form_data: dict) -> None:
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.maintenance_logs
			(
				maint_status_id,
				maint_started_date,
				maint_completed_date,
				maint_performed_by_technician_id,
				maint_performed_by_external_name,
				maint_description,
				maint_notes
			)
			VALUES
			(
				%s,
				%s,
				%s,
				%s,
				%s,
				%s,
				%s
			)
		"""
		values = (
			form_data["status_id"],
			form_data["started_date"],
			form_data["completed_date"],
			form_data["performed_by_technician_id"],
			form_data["performed_by_external_name"],
			form_data["description"],
			form_data["note"]
		)
		cursor.execute(query, values)
		conn.commit()
	
	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()

def update_maintenance_log(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.maintenance_logs
			SET
				maint_status_id = %s,
				maint_started_date = %s,
				maint_completed_date = %s,
				maint_performed_by_technician_id = %s,
				maint_performed_by_external_name = %s,
				maint_description = %s,
				maint_notes = %s
			WHERE
				maint_id = %s 
		"""
		values = (
			form_data["status_id"],
			form_data["started_date"],
			form_data["completed_date"],
			form_data["performed_by_technician_id"],
			form_data["performed_by_external_name"],
			form_data["description"],
			form_data["note"],
			form_data["maint_id"]
		)
		cursor.execute(query, values)

		conn.commit()
	
	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()