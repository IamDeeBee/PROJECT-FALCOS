# ============================================================
# File :        reservation_form.py
# Project :     UAV Management Dashboard
# Purpose :     Reservation Form Dialog.
#
# Description:
#		 Handles:
#			- Creation UI
# 			- Update UI
#
# Author :  Debe Okoye
# Created : 2026-07-08
# ============================================================

from app.config.constants import TABLE_MAPPING, FORM_VALID_MODES, FLIGHT_LOCATIONS
from app.database.reservation_repository import(
	get_active_pilots,
	get_operational_uav,
	get_reservation_statuses,
	create_reservation,
	update_reservation
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import(
	QComboBox,
	QDateTimeEdit,
	QDialog,
	QDoubleSpinBox,
	QFormLayout,
	QLineEdit,
	QTextEdit,
	QMessageBox,
	QPushButton,
	QVBoxLayout

)

# ============================================================
#  Reservation Form
# ============================================================
class ReservationForm(QDialog):
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
		self.resize(500,550)

		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Fields
		# ========================================================
		self.pilot_combo = QComboBox()
		self.uav_combo  = QComboBox()
		self.status_combo = QComboBox()

		self.start_input =  QDateTimeEdit()
		self.start_input.setCalendarPopup(True)
		self.start_input.setDisplayFormat("yyyy-MM-dd HH:mm")
		self.start_input.setDateTime(current)
		self.end_input =  QDateTimeEdit()
		self.end_input.setCalendarPopup(True)
		self.end_input.setDisplayFormat("yyyy-MM-dd HH:mm")
		self.end_input.setDateTime(current.addDays(1))

		self.location_combo = QComboBox()
		self.location_combo.addItems(FLIGHT_LOCATIONS)
		self.location_combo.setCurrentText("SPECIFIC")
		self.latitude_input = QDoubleSpinBox()
		self.latitude_input.setRange(-90.0 , 90.0)
		self.latitude_input.setDecimals(6)
		self.longitude_input = QDoubleSpinBox()
		self.longitude_input.setRange(-180.0 , 180.0)
		self.longitude_input.setDecimals(6)
		self.mission_type_input = QTextEdit()

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("Pilot" ,self.pilot_combo)
		form_layout.addRow("UAV" ,self.uav_combo)
		if self.mode == "update":
			form_layout.addRow("Status" ,self.status_combo)
		   
		form_layout.addRow("Planned Start" ,self.start_input)
		form_layout.addRow("Planned End" ,self.end_input)
		
		form_layout.addRow("Location" ,self.location_combo)
		form_layout.addRow("Latitude" ,self.latitude_input)
		form_layout.addRow("Longitude" ,self.longitude_input)
		form_layout.addRow("Mission Description" ,self.mission_type_input)
			
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
		self.load_active_pilots()
		self.load_operational_uav()
		if self.mode == "update":
			self.load_statuses()

		# ========================================================
		# Connect Signals
		# ========================================================
		self.location_combo.currentTextChanged.connect(self.update_location_fields)
		self.update_location_fields()

		# ========================================================
		# Load Existing data
		# ========================================================
		if self.mode == "update":
			self.load_record_data()

	# ========================================================
	#  Load Existing Record Data
	#  ======================================================== 
	def load_record_data(self) -> None:
		if not self.record_data :
			return
		
		pilot_index = self.pilot_combo.findData(self.record_data["reserv_pilot_id"])
		if pilot_index >=0 :
			self.pilot_combo.setCurrentIndex(pilot_index)
		uav_index = self.uav_combo.findData(self.record_data["reserv_asset_id"])
		if uav_index >= 0:
			self.uav_combo.setCurrentIndex(uav_index)
		status_index = self.status_combo.findData(self.record_data["reserv_status_id"])
		if status_index >= 0:
			self.status_combo.setCurrentIndex(status_index)

		if self.record_data["reserv_start"] is not None:
			self.start_input.setDateTime(self.record_data["reserv_start"])
		if self.record_data["reserv_end"] is not None:
			self.end_input.setDateTime(self.record_data["reserv_end"])

		location_index = self.location_combo.findText(self.record_data["reserv_flight_location"])
		if location_index >= 0:
			self.location_combo.setCurrentIndex(location_index)
		self.latitude_input.setValue(self.record_data["reserv_lat"])
		self.longitude_input.setValue(self.record_data["reserv_long"])
		self.mission_type_input.setPlainText(self.record_data["reserv_mission_type"])
		self.update_location_fields()
	
	# ========================================================
	# Load Active Pilots
	# ========================================================
	def load_active_pilots(self) -> None:
		try:
			rows = get_active_pilots()

			self.pilot_combo.clear()

			if not rows:
				self.pilot_combo.addItem("No Active Pilots Available", None)
				self.pilot_combo.setEnabled(False)
				return
			
			self.pilot_combo.setEnabled(True)

			for pilot_id, first_name, last_name, email in rows:
				if email:
					display_name = f"{first_name} {last_name} ({email})"
				else:
					display_name = f"{first_name} {last_name}"
				self.pilot_combo.addItem(display_name,pilot_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Pilot Error",str(e))

	# ========================================================
	# Load Operational UAV
	# ========================================================
	def load_operational_uav(self) -> None:
		try:
			rows = get_operational_uav()

			self.uav_combo.clear()

			if not rows:
				self.uav_combo.addItem("No Operational UAVs", None)
				self.uav_combo.setEnabled(False)
				return
			
			self.uav_combo.setEnabled(True)

			for asset_id, asset_nickname in rows:
				display_name = f"{asset_nickname}"
				self.uav_combo.addItem(display_name, asset_id)

		except Exception as e:
			QMessageBox.critical(self,"Load UAV Error",str(e))

	# ========================================================
	# Load Reservation Status
	# ========================================================
	def load_statuses(self) -> None:
		try:
			rows = get_reservation_statuses()

			self.status_combo.clear()

			if not rows:
				self.status_combo.addItem("No Reservation Status Available",None)
				self.status_combo.setEnabled(False)
				return

			self.status_combo.setEnabled(True)

			for status_id, status_name in rows:
				self.status_combo.addItem(status_name,status_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Reservation Status Error",str(e))

	# ========================================================
	# Update Location Fields
	# ========================================================
	def update_location_fields(self) -> None:

		location = self.location_combo.currentText()

		if location == "SPECIFIC":
			self.latitude_input.setEnabled(True)
			self.longitude_input.setEnabled(True)

		else:
			self.latitude_input.setValue(0.0)
			self.longitude_input.setValue(0.0)
			self.latitude_input.setEnabled(False)
			self.longitude_input.setEnabled(False)

	# ========================================================
	#  Retrieve Form Input Values 
	# ======================================================== 
	def get_form_data(self) -> dict:
		return{
			"pilot_id": self.pilot_combo.currentData(),
			"asset_id": self.uav_combo.currentData(),
			"status_id": self.status_combo.currentData(),
			"start": self.start_input.dateTime().toPyDateTime(),
			"end": self.end_input.dateTime().toPyDateTime(),
			"location": self.location_combo.currentText(),
			"latitude": self.latitude_input.value(),
			"longitude": self.longitude_input.value(),
			"mission_type": self.mission_type_input.toPlainText().strip()
		} 

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool: 
		# ====================================================
		# Pilot
		# ====================================================
		if form_data["pilot_id"] is None:
			QMessageBox.warning(
				self,
				"Validation Error",
				"Please select a pilot."
			)
			return False

		# ====================================================
		# UAV
		# ====================================================
		if form_data["asset_id"] is None:
			QMessageBox.warning(
				self,
				"Validation Error",
				"Please select a UAV."
			)
			return False

		# ====================================================
		# Planned Start / End
		# ====================================================
		if form_data["start"] >= form_data["end"]:
			QMessageBox.warning(
				self,
				"Validation Error",
				"The planned end time must be after the planned start time."
			)
			return False

		# ====================================================
		# Mission Description
		# ====================================================
		if not form_data["mission_type"]:
			QMessageBox.warning(
				self,
				"Validation Error",
				"Please enter a mission description."
			)
			return False

		# ====================================================
		# Specific Location
		# ====================================================
		if form_data["location"] == "SPECIFIC":

			if (
				(form_data["latitude"] > 90.0 or form_data["latitude"] < -90.0)or
				(form_data["longitude"] > 180.0 or form_data["longitude"] < -180.0)
			):
				QMessageBox.warning(
					self,
					"Validation Error",
					"Please enter a valid latitude and longitude."
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
			create_reservation(form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Created {self.table_name} for {self.pilot_combo.currentText()}"
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
			update_reservation(self.record_data["reserv_id"],form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))
