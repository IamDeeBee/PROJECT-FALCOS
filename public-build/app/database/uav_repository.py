# ============================================================
# File:         uav_repository.py
# Project:      UAV Management Dashboard
# Purpose:      UAV database operations.
#
# Description:
#       Handles:
#           - company retrieval
#           - certification retrieval
#           - UAV status retrieval
#           - UAV creation
#           - UAV updates
#
# Author: Debe Okoye
# Created: 2026-08-26
# ============================================================
from app.config.constants import DB_SCHEMA, DEMO_MODE
from app.database.connection import get_connection

def get_companies():
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

def get_uav_statuses():
	if DEMO_MODE:
		return []
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				SELECT
					status_id,
					status_name
				FROM {DB_SCHEMA}.fleet_asset_status
				ORDER BY
					status_id
			"""
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()
	
def create_uav(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.fleet_asset
			(
				asset_serial_number,
				asset_company_id,
				asset_model,
				asset_nickname,
				asset_cert_id,
				asset_status_id,
				asset_flight_hours,
				asset_faa_registration,
				asset_issued_date,
				asset_expiry_date
			)
			VALUES
			(
				%s,
				%s,
				%s,
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
			form_data["serial_number"],
			form_data["company_id"],
			form_data["model"],
			form_data["nickname"],
			form_data["certification_id"],
			form_data["status_id"],
			form_data["flight_hours"],
			form_data["faa_registration"],
			form_data["issued_date"],
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
	
def update_uav(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				UPDATE {DB_SCHEMA}.fleet_asset
				SET
					asset_serial_number = %s,
					asset_company_id = %s,
					asset_model = %s,
					asset_nickname = %s,
					asset_cert_id = %s,
					asset_status_id = %s,
					asset_faa_registration = %s,
					asset_issued_date = %s,
					asset_expiry_date = %s
				WHERE
					asset_id = %s
			"""
		values = (
			form_data["serial_number"],
			form_data["company_id"],
			form_data["model"],
			form_data["nickname"],
			form_data["certification_id"],
			form_data["status_id"],
			form_data["faa_registration"],
			form_data["issued_date"],
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