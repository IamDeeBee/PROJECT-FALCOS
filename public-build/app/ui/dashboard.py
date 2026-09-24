# ============================================================
# File:         dashboard.py
# Project:      UAV Management Dashboard
# Purpose:      Main application dashboard controller.


# Description:
#       Coordinates:
#       - application layout
#       - tab navigation
#       - dashboard pages
#       - monitor pages
#       - theme integration


# Author: Debe Okoye
# Created: 2026-06-02
# ============================================================
from datetime import datetime
from app.config.constants import DEMO_MODE
from app.database.connection import get_connection
from app.ui.dashboard_widgets import (
	build_dashboard_page,
	refresh_dashboard
)
from app.ui.monitor import build_monitor_page
from app.ui.sidebar import build_sidebar
from app.ui.proficiency_matrix import build_proficiency_page
from app.styling.theme import (
	apply_theme,
	toggle_theme
)
from PyQt6.QtCore import (
	QDateTime
)
from PyQt6.QtWidgets import(
	QFrame,
	QHBoxLayout,
	QLabel,
	QMainWindow,
	QMessageBox,
	QPushButton,
	QStackedWidget,
	QTabBar,
	QVBoxLayout,
	QWidget
)

# ============================================================
# Main Dashboard Window
# ============================================================
class DashboardWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowTitle("UAV Engineering Dashboard[DEMO]")
		self.resize(1320, 820)
		self.dark_mode = True

		self.central = QWidget()
		self.setCentralWidget(self.central)

		outer_layout = QHBoxLayout(self.central)
		outer_layout.setContentsMargins(12, 12, 12, 12)
		outer_layout.setSpacing(12)

		self.main_content = self._build_main_content()
		self.sidebar = build_sidebar(self)

		outer_layout.addWidget(self.sidebar, 1)
		outer_layout.addWidget(self.main_content, 4)

		apply_theme(self)

		if DEMO_MODE:
			self.show_supabase_integration_popup()
		else:
			refresh_dashboard(self)

	# ======================================================== 
	# Main Content Construction 
	# ========================================================
	def _build_main_content(self) -> QWidget:
		wrapper = QWidget()
		layout = QVBoxLayout(wrapper)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(10)

		header = QFrame()
		header_layout = QHBoxLayout(header)
		header_layout.setContentsMargins(10, 8, 10, 8)
		header_layout.setSpacing(8)

		self.tabs = QTabBar()
		self.tabs.addTab("Summary Dashboard")
		self.tabs.addTab("Monitor")
		self.tabs.addTab("Pilot Proficiency Tracker")
		self.tabs.currentChanged.connect(self.on_tab_changed)
		header_layout.addWidget(self.tabs, 2)

		toggle_label = QLabel("Dark / Light")
		header_layout.addWidget(toggle_label)

		self.theme_toggle = QPushButton("Dark")
		self.theme_toggle.setCheckable(True)
		self.theme_toggle.setChecked(True)
		self.theme_toggle.clicked.connect(lambda: toggle_theme(self))
		header_layout.addWidget(self.theme_toggle)
		
		self.tab_stack = QStackedWidget()
		self.tab_stack.addWidget(build_dashboard_page(self))
		self.tab_stack.addWidget(build_monitor_page(self))
		self.tab_stack.addWidget(build_proficiency_page(self))

		layout.addWidget(header)
		layout.addWidget(self.tab_stack,1)
		return wrapper
	
	# ======================================================== 
	# Tab Navigation 
	# ========================================================
	def on_tab_changed(self, idx: int) -> None:
		self.tab_stack.setCurrentIndex(idx)

	# ======================================================== 
	# Test Database Connection
	# ========================================================
	def test_database_connection(self) -> None :
		# Tests PostgreSQL database connection.
		try:
			conn = get_connection()

			db_info = conn.get_dsn_parameters()

			db_name = db_info.get("dbname","Unknown")
			db_host = db_info.get("host","Unknown")
			db_user = db_info.get("user","Unknown")

			self.db_status_label.setText("Status: Connected")
			self.db_name_label.setText( f"Database: {db_name}" ) 
			self.db_host_label.setText( f"Host: {db_host}")
			self.db_user_label.setText( f"User: {db_user}")
			self.db_last_refresh_label.setText(f"Last Refresh: {datetime.now().strftime('%H:%M:%S')}")

			QMessageBox.information( self, "Database Success", "Successfully connected to PostgreSQL." )

			conn.close()

		except Exception as e :
			self.db_status_label.setText( "Status: Failed" )

			QMessageBox.critical( self, "Database Error", str(e) )

	# ========================================================
	# Activity Logger
	# ========================================================
	def log_activity(self, message: str) -> None:

		# Adds activity message to dashboard activity feed.
		timestamp = QDateTime.currentDateTime()

		formatted_time = timestamp.toString("hh:mm:ss AP")

		self.activity_feed.insertItem(0, f"[{formatted_time}] {message}")


	def show_supabase_integration_popup(self):
		QMessageBox.information(
			self,
			"Supabase Integration",
			"Database integration is not configured in this version.\n\n"
			"This build is intended for interface evaluation and feedback."
		)
	