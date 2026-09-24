# ============================================================
# File:         reservation_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Flight reservation database operations.
#
# Description:
#       Handles:
#           - active pilot retrieval
#           - operational UAV retrieval
#           - reservation status retrieval
#           - reservation creation
#           - reservation updates
#
# Author: Debe Okoye
# Created: 2026-08-26
# ============================================================
from app.config.constants import DB_SCHEMA, DEMO_MODE
from app.database.connection import get_connection

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

def get_operational_uav():
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
			WHERE
				fa.asset_status_id = (
					SELECT status_id
					FROM {DB_SCHEMA}.fleet_asset_status
					WHERE status_name = 'OPERATIONAL'
				)
			ORDER BY
				fa.asset_nickname
		"""
		
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def get_reservation_statuses():
	if DEMO_MODE:
		return []
	
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			SELECT
				status_id,
				status_name
			FROM {DB_SCHEMA}.flight_reservations_status
			ORDER BY
				status_id
		"""
		cursor.execute(query)
		return cursor.fetchall()

	finally:
		cursor.close()
		conn.close()

def create_reservation(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.flight_reservations
			(
				reserv_pilot_id,
				reserv_asset_id,
				reserv_start,
				reserv_end,
				reserv_flight_location,
				reserv_lat,
				reserv_long,
				reserv_mission_type
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
				%s
			)
		"""
		latitude = (
			form_data["latitude"]
			if form_data["location"] == "SPECIFIC"
			else None
		)
		
		longitude = (
			form_data["longitude"]
			if form_data["location"] == "SPECIFIC"
			else None
		)
		
		values = (
			form_data["pilot_id"],
			form_data["asset_id"],
			form_data["start"],
			form_data["end"],
			form_data["location"],
			latitude,
			longitude,
			form_data["mission_type"]
		)

		cursor.execute(query, values)
		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()

def update_reservation(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.flight_reservations
			SET
				reserv_pilot_id = %s,
				reserv_asset_id = %s,
				reserv_status_id = %s,
				reserv_start = %s,
				reserv_end = %s,
				reserv_flight_location = %s,
				reserv_lat = %s,
				reserv_long = %s,
				reserv_mission_type = %s
				
			WHERE
				reserv_id = %s
		"""
		latitude = (
			form_data["latitude"]
			if form_data["location"] == "SPECIFIC"
			else None
		)
		
		longitude = (
			form_data["longitude"]
			if form_data["location"] == "SPECIFIC"
			else None
		)
		
		values = (
			form_data["pilot_id"],
			form_data["asset_id"],
			form_data["status_id"],
			form_data["start"],
			form_data["end"],
			form_data["location"],
			latitude,
			longitude,
			form_data["mission_type"],
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
