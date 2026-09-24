# ============================================================
# File :        flight_log_form.py
# Project :     UAV Management Dashboard
# Purpose :     Flight Log Form Dialog.
#
# Description:
#       Handles:
#           - Creation UI
#           - Update UI
#           - INSERT Operation
#           - UPDATE Operation
#           - PostgreSQL Integration
#
# Author :  Debe Okoye
# Created : 2026-07-08
# ============================================================

from app.config.constants import TABLE_MAPPING, FORM_VALID_MODES
from app.database.flight_log_repository import (
	get_completed_reservations,
	get_reservation_details,
	create_flight_log,
	update_flight_log
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import(
	QCheckBox,
	QComboBox,
	QDateTimeEdit,
	QDialog,
	QFormLayout,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QTextEdit,
	QVBoxLayout

)

# ============================================================
#  Flight Log Form
# ============================================================
class FlightLogForm(QDialog):
	def __init__(self, window, mode, table_name, record_data = None):
		super().__init__(window)

		# ========================================================
		# Instance variable and validation
		# ========================================================
		self.window = window
		self.mode = mode
		self.record_data = record_data
		self.table_name = table_name
		if self.mode not in FORM_VALID_MODES:
			QMessageBox.critical(self,"Configuration Error",f"Invalid Form mode : {self.mode}.")
			self.close()
			return
		if self.table_name is None:
			QMessageBox.critical(self,"Configuration Error","Table name was not specified")
			self.close()
			return
		if self.table_name not in TABLE_MAPPING:
			QMessageBox.critical(self,"Configuration Error",f"Unknown Table : {self.table_name}")
			self.close()
			return
		
		# ========================================================
		# Derived Variables
		# ========================================================
		self.db_table = TABLE_MAPPING[self.table_name]
		current = QDateTime.currentDateTime()
		
		# ========================================================
		# Window Configuration
		# ========================================================
		self.setWindowTitle(f"{self.mode.title()} {self.table_name}")
		self.resize(400,250)
		
		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Field
		# ========================================================
		self.reservation_combo = QComboBox()

		self.reservation_id_input = QLineEdit()
		self.reservation_id_input.setReadOnly(True)

		self.pilot_input = QLineEdit()
		self.pilot_input.setReadOnly(True)

		self.uav_input = QLineEdit()
		self.uav_input.setReadOnly(True)

		self.location_input = QLineEdit()
		self.location_input.setReadOnly(True)

		self.status_input = QLineEdit()
		self.status_input.setReadOnly(True)

		self.mission_type_input = QTextEdit()
		self.mission_type_input.setReadOnly(True)

		self.actual_start_input = QDateTimeEdit()
		self.actual_start_input.setCalendarPopup(True)
		self.actual_start_input.setDateTime(current)
		
		self.actual_end_input = QDateTimeEdit()
		self.actual_end_input.setCalendarPopup(True)
		self.actual_end_input.setDateTime(current.addDays(1))

		self.preflight_check_input = QCheckBox()
		self.postflight_check_input = QCheckBox()

		self.incidents_input = QTextEdit()
		self.notes_input = QTextEdit()

		# ========================================================
		# Form Rows
		# ========================================================
		if self.mode == "update":
			form_layout.addRow("Reservation ID #", self.reservation_id_input)
		else:
			form_layout.addRow("Reservation", self.reservation_combo)

		form_layout.addRow("Pilot", self.pilot_input)
		form_layout.addRow("UAV", self.uav_input)
		form_layout.addRow("Location", self.location_input)
		form_layout.addRow("Status", self.status_input)
		
		form_layout.addRow("Mission Description", self.mission_type_input)

		form_layout.addRow("Actual Start", self.actual_start_input)
		form_layout.addRow("Actual End", self.actual_end_input)

		form_layout.addRow("Pre-Flight Check", self.preflight_check_input)
		form_layout.addRow("Post-Flight Check",self.postflight_check_input)

		form_layout.addRow("Incidents" ,self.incidents_input)
		form_layout.addRow("Notes", self.notes_input)			
		
		# ========================================================
		# Submit Button
		# ========================================================
		btn_name = f"{self.mode.title()} {self.table_name}"
		submit_btn = QPushButton(btn_name)
		if self.mode == "create":
			submit_btn.clicked.connect(self.create_entry)
		else :
			submit_btn.clicked.connect(self.update_entry)
		
		# ========================================================
		# Organize Layout
		# ========================================================
		layout.addLayout(form_layout)
		layout.addWidget(submit_btn)

		# ========================================================
		# Populate Combo Boxes
		# ========================================================
		self.load_completed_reservations()

		# ========================================================
		# Connect Signals
		# ========================================================
		self.reservation_combo.currentIndexChanged.connect(self.populate_reservation_details)
		self.populate_reservation_details()

		# ========================================================
		# Load Existing data
		# ========================================================
		if self.mode == "update":
			self.reservation_combo.setEnabled(False)
			self.load_record_data()

	# ========================================================
	#  Load Completed Reservations
	#  ======================================================== 
	def load_completed_reservations(self) -> None:
		try:
			rows = get_completed_reservations()

			self.reservation_combo.clear()

			if not rows:
				self.reservation_combo.addItem(
					"No Completed Reservations",
					None
				)
				self.reservation_combo.setEnabled(False)
				return

			self.reservation_combo.setEnabled(True)

			for reserv_id, first_name, last_name, asset_name, reserv_start in rows:

				display_name = (
					f"#{reserv_id} | "
					f"{asset_name} | "
					f"{first_name} {last_name} | "
					f"{reserv_start:%Y-%m-%d %H:%M}"
				)

				self.reservation_combo.addItem(display_name, reserv_id)

		except Exception as e:
			QMessageBox.critical(
				self,
				"Load Reservation Error",
				str(e)
			)

	# ========================================================
	# Populate Reservation Details
	# ======================================================== 
	def populate_reservation_details(self) -> None:
		reserv_id = self.reservation_combo.currentData()
		
		if reserv_id is None:
			self.clear_reservation_details()
			return
		
		try:
			row = get_reservation_details(reserv_id)

			if row is None:
				self.clear_reservation_details()
				return
			
			if row:
				(first_name,last_name,asset_nickname,location,status,mission_type) = row

				self.pilot_input.setText(f"{first_name} {last_name}")
				self.uav_input.setText(asset_nickname)
				self.location_input.setText(location)
				self.status_input.setText(status)
				self.mission_type_input.setPlainText(mission_type)

		except Exception as e:
			QMessageBox.critical(
				self,
				"Reservation Error",
				str(e)
			)

	# ========================================================
	# Clear Reservation Details
	# ======================================================== 
	def clear_reservation_details(self) -> None :
		self.pilot_input.clear()
		self.uav_input.clear()
		self.location_input.clear()
		self.status_input.clear()
		self.mission_type_input.clear()

	# ========================================================
	# Load Existing Record Data
	# ======================================================== 
	def load_record_data(self) -> None: 
		if not self.record_data :
			return
		
		reservation_index = self.reservation_combo.findData(self.record_data["log_reserv_id"])
		if reservation_index >= 0:
			self.reservation_combo.setCurrentIndex(reservation_index)

		self.reservation_id_input.setText(str(self.record_data["log_reserv_id"]))

		if self.record_data["log_actual_start"] is not None:
			self.actual_start_input.setDateTime(self.record_data["log_actual_start"])
		if self.record_data["log_actual_end"] is not None:
			self.actual_end_input.setDateTime(self.record_data["log_actual_end"])
		
		self.preflight_check_input.setChecked(self.record_data["log_pre_flight_check"])
		self.postflight_check_input.setChecked(self.record_data["log_post_flight_check"])
		
		self.incidents_input.setPlainText(self.record_data["log_incidents"] or "")
		self.notes_input.setPlainText(self.record_data["log_notes"] or "")

	# ========================================================
	#  Retrieve Form Input Values 
	#  ======================================================== 
	def get_form_data(self) -> dict: 
		return {
			"reserv_id": self.reservation_combo.currentData(),
			"actual_start": self.actual_start_input.dateTime().toPyDateTime(),
			"actual_end": self.actual_end_input.dateTime().toPyDateTime(),
			"pre_flight_check": self.preflight_check_input.isChecked(),
			"post_flight_check": self.postflight_check_input.isChecked(),
			"incidents": self.incidents_input.toPlainText().strip() or None,
			"notes": self.notes_input.toPlainText().strip() or None
    	}
	
	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool: 
		# ====================================================
		# Reservation
		# ====================================================
		if form_data["reserv_id"] is None:
			QMessageBox.warning(
				self,
				"Validation Error",
				"Please select a reservation."
			)
			return False

		# ====================================================
		# Actual Flight Times
		# ====================================================
		if form_data["actual_start"] >= form_data["actual_end"]:
			QMessageBox.warning(
				self,
				"Validation Error",
				"Actual end time must be after the actual start time."
			)
			return False

		return True
	
	# ========================================================  
	# Creation Logic  
	# ========================================================
	def create_entry(self) -> None:
		form_data = self.get_form_data()

		if not self.validate_form_data(form_data):
			return
		
		try:
			create_flight_log(form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Created {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} created successfully.")

			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Create Error",str(e))

	# ========================================================
	# Update Logic
	# ========================================================
	def update_entry(self) -> None:
		form_data = self.get_form_data()

		if not self.validate_form_data(form_data):
			return

		try:
			update_flight_log(self.record_data["log_id"], form_data)
			
			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))