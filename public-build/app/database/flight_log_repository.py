# ============================================================
# File:         flight_log_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Flight log database operations.
#
# Description:
#       Handles:
#           - completed reservation retrieval
#           - reservation detail retrieval
#           - flight log creation
#           - flight log updates
#
# Author: Debe Okoye
# Created: 2026-08-25
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA, DEMO_MODE

def get_completed_reservations():
	if DEMO_MODE:
		return []
		
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				SELECT
					fr.reserv_id,
					pe.person_first_name,
					pe.person_last_name,
					fa.asset_nickname,
					fr.reserv_start
				FROM {DB_SCHEMA}.flight_reservations fr
				INNER JOIN {DB_SCHEMA}.pilot p
					ON fr.reserv_pilot_id = p.pilot_id
				INNER JOIN {DB_SCHEMA}.person pe
					ON p.pilot_person_id = pe.person_id
				INNER JOIN {DB_SCHEMA}.fleet_asset fa
					ON fr.reserv_asset_id = fa.asset_id
				WHERE
					fr.reserv_status_id = (
						SELECT status_id
						FROM {DB_SCHEMA}.flight_reservations_status
						WHERE status_name = 'COMPLETED'
					)
				ORDER BY
					fr.reserv_start DESC,
					pe.person_last_name
			"""
		
		cursor.execute(query)
		
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_reservation_details(reserv_id: int):
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				SELECT
					pe.person_first_name,
					pe.person_last_name,
					fa.asset_nickname,
					fr.reserv_flight_location,
					frs.status_name,
					fr.reserv_mission_type
					
				FROM {DB_SCHEMA}.flight_reservations fr
				INNER JOIN {DB_SCHEMA}.pilot p
					ON fr.reserv_pilot_id = p.pilot_id
				INNER JOIN {DB_SCHEMA}.person pe
					ON p.pilot_person_id = pe.person_id
				INNER JOIN {DB_SCHEMA}.fleet_asset fa
					ON fr.reserv_asset_id = fa.asset_id
				INNER JOIN {DB_SCHEMA}.flight_reservations_status frs
					ON fr.reserv_status_id = frs.status_id
				WHERE
					fr.reserv_id = %s
			"""
		
		cursor.execute(query, (reserv_id,))
		
		row = cursor.fetchone()
	
	finally:
		cursor.close()
		conn.close()

def create_flight_log(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				INSERT INTO {DB_SCHEMA}.flight_logs
				(
					log_reserv_id,
					log_actual_start,
					log_actual_end,
					log_pre_flight_check,
					log_post_flight_check,
					log_incidents,
					log_notes
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
			form_data["reserv_id"],
			form_data["actual_start"],
			form_data["actual_end"],
			form_data["pre_flight_check"],
			form_data["post_flight_check"],
			form_data["incidents"],
			form_data["notes"]
		)
		cursor.execute(query, values)
		
		conn.commit()

	except Exception:
			conn.rollback()
			raise
	
	finally:
		cursor.close()
		conn.close()

def update_flight_log(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.flight_logs
			SET
				log_reserv_id = %s,
				log_actual_start = %s,
				log_actual_end = %s,
				log_pre_flight_check = %s,
				log_post_flight_check = %s,
				log_incidents = %s,
				log_notes = %s
			WHERE
				log_id = %s
		"""
		values = (
			form_data["reserv_id"],
			form_data["actual_start"],
			form_data["actual_end"],
			form_data["pre_flight_check"],
			form_data["post_flight_check"],
			form_data["incidents"],
			form_data["notes"],
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