# ============================================================
# File:         certification_repository.py
# Project:      UAV Management Dashboard
# Purpose:      Certification database operations.
#
# Description:
#       Handles:
#           - certification creation
#           - certification updates
#
# Author: Debe Okoye
# Created: 2026-08-24
# ============================================================
from app.database.connection import get_connection
from app.config.constants import DB_SCHEMA

def create_certification(form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			INSERT INTO {DB_SCHEMA}.certifications
			(
				cert_name,
				cert_provider,
				cert_provider_website

			)
			VALUES
			(
				%s,
				%s,
				%s
			)
		"""
		values = (
			form_data["name"],
			form_data["provider"],
			form_data["provider_website"]
		)
		cursor.execute(query, values)

		conn.commit()

	except Exception as e:
		conn.rollback()
		raise

	finally:
		cursor.close()
		conn.close()

def update_certification(record_id: int, form_data: dict) -> None:
	conn = get_connection()
	cursor = conn.cursor()

	try:
		query = f"""
			UPDATE {DB_SCHEMA}.certifications
			SET
				cert_name = %s,
				cert_provider = %s,
				cert_provider_website = %s
			WHERE
				cert_id = %s
		"""
		values = (
			form_data["name"],
			form_data["provider"],
			form_data["provider_website"],
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