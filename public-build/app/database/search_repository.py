# ============================================================
# File:         search_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Search and record database operations.
#
# Description:
#       Handles:
#           - record searches
#           - record retrieval
#           - record deletion
#
# Author: Debe Okoye
# Created: 2026-08-24
# ============================================================
from app.config.constants import DB_SCHEMA
from app.database.connection import get_connection
from psycopg2.extras import RealDictCursor

def search_records(db_view: str, search_column: str, search_value: str):
	conn = get_connection()

	try:
		query = f"""
			SELECT *
			FROM {DB_SCHEMA}.{db_view}
			WHERE {search_column}::TEXT ILIKE %s
		"""

		with conn.cursor() as cursor:
			cursor.execute(query, (f"{search_value}%",))

			rows = cursor.fetchall()
			column_names = [desc[0] for desc in cursor.description]

			return column_names, rows

	finally:
		conn.close()


def get_record(table: str, primary_key: str, record_id):
	conn = get_connection()

	try:
		query = f"""
			SELECT *
			FROM {DB_SCHEMA}.{table}
			WHERE {primary_key} = %s
		"""

		with conn.cursor(cursor_factory=RealDictCursor) as cursor:
			cursor.execute(query, (record_id,))
			return cursor.fetchone()

	finally:
		conn.close()


def delete_record(table: str, primary_key: str, record_id):
	conn = get_connection()

	try:
		query = f"""
			DELETE FROM {DB_SCHEMA}.{table}
			WHERE {primary_key} = %s
		"""

		with conn.cursor() as cursor:
			cursor.execute(query, (record_id,))

		conn.commit()

	except Exception:
		conn.rollback()
		raise

	finally:
		conn.close()