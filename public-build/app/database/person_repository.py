# ============================================================
# File:         person_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Person database operations.
#
# Description:
#       Handles:
#           - person creation
#           - person updates
#
# Author: Debe Okoye
# Created: 2026-08-26
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA

def create_person(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.person
			(
				person_first_name,
				person_last_name,
				person_primary_email
			)
			VALUES
			(
				%s,
				%s,
				%s
			)
		"""
		values = (
			form_data["first_name"],
			form_data["last_name"],
			form_data["primary_email"]
		)
		cursor.execute(query, values)
		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:	
		cursor.close()
		conn.close()

def update_person(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
				UPDATE {DB_SCHEMA}.person
				SET
					person_first_name = %s,
					person_last_name = %s,
					person_primary_email = %s
					
				WHERE
					person_id = %s
			"""
		values = (
			form_data["first_name"],
			form_data["last_name"],
			form_data["primary_email"],
			record_id
		)
		cursor.execute(query, values)

	except Exception:
		conn.rollback()
		raise

	finally:	
		cursor.close()
		conn.close()
