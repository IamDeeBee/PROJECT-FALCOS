# ============================================================
# File:         maintenance_order_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Maintenance order database operations.
#
# Description:
#       Handles:
#           - available UAV retrieval
#           - personnel retrieval
#           - maintenance status retrieval
#           - maintenance order creation
#           - maintenance order updates
#
# Author: Debe Okoye
# Created: 2026-08-26
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA, DEMO_MODE

def get_available_uav():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				fa.asset_id,
				fa.asset_nickname
			FROM {DB_SCHEMA}.fleet_asset fa
			WHERE NOT EXISTS
			(
				SELECT 1
				FROM {DB_SCHEMA}.maintenance_logs ml
				INNER JOIN {DB_SCHEMA}.maintenance_logs_status mls
					ON ml.maint_status_id = mls.status_id
				WHERE
					ml.maint_asset_id = fa.asset_id
					AND mls.status_name IN ('REPORTED', 'IN_PROGRESS')
			)
			ORDER BY
				fa.asset_nickname
		"""
		
		cursor.execute(query)

		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()


def get_personnel():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				person_id,
				pe.person_first_name,
				pe.person_last_name,
				pe.person_primary_email
			FROM {DB_SCHEMA}.person pe
			ORDER BY
				pe.person_last_name, pe.person_first_name
		"""
		
		cursor.execute(query)

		return cursor.fetchall()

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

def create_maintenance_order(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.maintenance_logs
			(
				maint_asset_id,
				maint_type,
				maint_reported_by_person_id,
				maint_reported_by_external_name,
				maint_reported_date,
				maint_reason
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
			form_data["asset_id"],
			form_data["maintenance_type"],
			form_data["reported_by_person_id"],
			form_data["reported_by_external_name"],
			form_data["reported_date"],
			form_data["reason"]
		)

		cursor.execute(query, values)
		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()

def update_maintenance_order(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.maintenance_logs
			SET
				maint_asset_id = %s,
				maint_type = %s,
				maint_status_id = %s,
				maint_reported_by_person_id = %s,
				maint_reported_by_external_name = %s,
				maint_reported_date = %s,
				maint_reason = %s
			WHERE
				maint_id = %s
		"""
		values = (
			form_data["asset_id"],
			form_data["maintenance_type"],
			form_data["status_id"],
			form_data["reported_by_person_id"],
			form_data["reported_by_external_name"],
			form_data["reported_date"],
			form_data["reason"],
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