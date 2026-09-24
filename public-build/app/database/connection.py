# ============================================================
# File:         connection.py
# Project:      UAV Management Dashboard
# Purpose:      Handles PostgreSQL database connections.


# Description:
#       Provides reusable database connection function
#       for the entire application.


# Author: Debe Okoye
# Created: 2026-06-03
# ============================================================
from PyQt6.QtWidgets import(
	QMessageBox
)

from app.config.constants import DEMO_MODE

def get_connection():
	if DEMO_MODE:
		QMessageBox.information(
			None,
			"Supabase Integration",
			"Database integration is not configured in this version.\n\n"
			"This build is intended for interface evaluation and feedback."
		)
		return None