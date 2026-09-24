# ============================================================
# File:         proficiency_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Proficiency database operations.
#
# Description:
#       Handles:
#       - proficiency data retrieval
#       - proficiency level updates
#
# Author: Debe Okoye
# Created: 2026-08-24
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA
from psycopg2.extras import RealDictCursor

# ============================================================
# Pull Pilot Proficiency Data
# ============================================================
def get_proficiency_data():
	conn = get_connection()

	try:
		query = f"""
			SELECT
				*
			FROM {DB_SCHEMA}.vw_all_pilot_proficiency;
		"""
		with conn.cursor(cursor_factory=RealDictCursor) as cursor:
			cursor.execute(query)
			return cursor.fetchall()

	finally:
		conn.close()

def update_proficiency_levels(changes):
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
					UPDATE {DB_SCHEMA}.pilot_proficiency
					SET
						pilprof_level = %s
					WHERE
						pilprof_id = %s
				"""
		
		for record_id, change in changes.items():
			cursor.execute(
				query,
				(change["level"], record_id)
			)

		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()