# ============================================================
# File :        pilot_form.py
# Project :     UAV Management Dashboard
# Purpose :     Pilot Form Dialog.
#
# Description:
#       Handles:
#           - Creation UI
#           - Update UI
#
# Author :  Debe Okoye
# Created : 2026-07-08
# ============================================================

from app.config.constants import TABLE_MAPPING, FORM_VALID_MODES
from app.database.pilot_repository import (
	get_available_personnel,
	get_all_pilots,
	get_person_details,
	get_pilot_statuses,
	create_pilot,
	update_pilot
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtWidgets import(
	QAbstractSpinBox,
	QComboBox,
	QDialog,
	QDoubleSpinBox,
	QFormLayout,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QVBoxLayout
)

# ============================================================
# Pilot Form
# ============================================================
class PilotForm(QDialog):
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
		
		# ========================================================
		# Window Configuration
		# ========================================================
		self.setWindowTitle(f"{self.mode.title()} {self.table_name}")
		self.resize(400,300)
		
		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Field
		# ========================================================
		self.person_id_combo = QComboBox()

		self.first_name_input= QLineEdit()
		self.first_name_input.setReadOnly(True)

		self.last_name_input= QLineEdit()
		self.last_name_input.setReadOnly(True)

		self.primary_email_input= QLineEdit()
		self.primary_email_input.setReadOnly(True)

		self.secondary_email_input = QLineEdit()

		self.status_combo = QComboBox()

		self.flight_hours_input = QDoubleSpinBox()
		self.flight_hours_input.setReadOnly(self.mode == "update")
		self.flight_hours_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.flight_hours_input.setDecimals(2)
		self.flight_hours_input.setRange(0.00, 9999.99)
		self.flight_hours_input.setValue(0.00)
		self.flight_hours_input.setSuffix(" hrs")

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("Personnel",self.person_id_combo)

		form_layout.addRow("First Name", self.first_name_input)
		form_layout.addRow("Last Name", self.last_name_input)
		form_layout.addRow("Primary Email", self.primary_email_input)

		form_layout.addRow("Secondary Email", self.secondary_email_input)
		form_layout.addRow("Status",self.status_combo)
		form_layout.addRow("Total Flight Hours", self.flight_hours_input)

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
		if self.mode == "create":
			self.load_person()
		else :
			self.load_all_pilots()

		self.load_statuses()
		if self.mode == "create":
			self.status_combo.setCurrentText("INACTIVE")
			self.status_combo.setEnabled(False)
		else :
			self.status_combo.setEnabled(True)

		# ========================================================
		# Connect Signals
		# ========================================================
		self.person_id_combo.currentIndexChanged.connect(self.populate_person_details)
		self.populate_person_details()

		# ========================================================
		# Load Existing data
		# ========================================================
		if self.mode == "update":
			self.load_record_data()

	# ========================================================
	# Load Personnel
	# ======================================================== 
	def load_person(self) -> None: 	
		try:
			rows = get_available_personnel()

			self.person_id_combo.clear()

			if not rows:
				self.person_id_combo.addItem("No Available Personnel", None)
				self.person_id_combo.setEnabled(False)
				return

			self.person_id_combo.setEnabled(True)

			for person_id, first_name, last_name, email in rows:

				if email:
					display_name = f"{first_name} {last_name} ({email})"
				else:
					display_name = f"{first_name} {last_name}"

				self.person_id_combo.addItem(display_name, person_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Personnel Error",str(e))

	# ========================================================
	# Load Pilots
	# ========================================================
	def load_all_pilots(self) -> None:
		try:
			rows = get_all_pilots()

			# ====================================================
			# Populate Combo Box
			# ====================================================
			self.person_id_combo.clear()

			if not rows:
				self.person_id_combo.addItem("No Pilots Available", None)
				self.person_id_combo.setEnabled(False)
				return

			self.person_id_combo.setEnabled(True)

			for person_id, first_name, last_name, email in rows:
				if email:
					display_name = f"{first_name} {last_name} ({email})"
				else:
					display_name = f"{first_name} {last_name}"

				self.person_id_combo.addItem(display_name, person_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Pilot Error",str(e))

	# ========================================================
	# Populate Personnel Details
	# ======================================================== 
	def populate_person_details(self) -> None: 
		person_id = self.person_id_combo.currentData()
		
		if person_id is None:
			self.clear_person_details()
			return

		try:
			row = get_person_details(person_id)

			if row:
				(
					first_name,
					last_name,
					email
				) = row

				self.first_name_input.setText(first_name)
				self.last_name_input.setText(last_name)
				self.primary_email_input.setText(email or "")

		except Exception as e:
			QMessageBox.critical(self, "Personnel Error", str(e))

	# ========================================================
	# Clear Personnel Details
	# ======================================================== 
	def clear_person_details(self) -> None:
		self.first_name_input.clear()
		self.last_name_input.clear()
		self.primary_email_input.clear()

	# ========================================================
	# Load Pilot Status
	# ======================================================== 
	def load_statuses(self) -> None:
		try:
			rows = get_pilot_statuses()

			self.status_combo.clear()

			if not rows:
				self.status_combo.addItem("No Pilot Status Available",None)
				self.status_combo.setEnabled(False)
				return

			self.status_combo.setEnabled(True)

			for status_id, status_name in rows:
				self.status_combo.addItem(status_name,status_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Pilot Status Error",str(e))

	# ========================================================
	# Load Existing Record Data
	# ======================================================== 
	def load_record_data(self) -> None:
		if not self.record_data:
			return

		person_index = self.person_id_combo.findData(self.record_data["pilot_person_id"])
		if person_index >= 0:
			self.person_id_combo.setCurrentIndex(person_index)

		self.secondary_email_input.setText(self.record_data["pilot_secondary_email"] or "")

		status_index = self.status_combo.findData(self.record_data["pilot_status_id"])
		if status_index >= 0:
			self.status_combo.setCurrentIndex(status_index)

		self.flight_hours_input.setValue(float(self.record_data["pilot_flight_hours"] or 0))
	
	# ========================================================
	# Retrieve Form Input Values 
	# ======================================================== 
	def get_form_data(self) -> dict:
		return {
			"person_id": self.person_id_combo.currentData(),
			"secondary_email": self.secondary_email_input.text().strip() or None,
			"status_id": self.status_combo.currentData(),
			"flight_hours": self.flight_hours_input.value()
		}

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool: 
		# ====================================================
		# Personnel
		# ====================================================
		if form_data["person_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select personnel.")
			return False

		# ====================================================
		# Secondary Email
		# ====================================================
		if (form_data["secondary_email"] and "@" not in form_data["secondary_email"]):
			QMessageBox.warning(self,"Validation Error","Please enter a valid secondary email address.")
			return False

		# ====================================================
		# Pilot Status
		# ====================================================
		if form_data["status_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a pilot status.")
			return False

		# ====================================================
		# Flight Hours
		# ====================================================
		if form_data["flight_hours"] < 0:
			QMessageBox.warning(self,"Validation Error","Flight hours cannot be negative.")
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
			create_pilot(form_data)

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
			update_pilot(self.record_data["pilot_id"],form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))
