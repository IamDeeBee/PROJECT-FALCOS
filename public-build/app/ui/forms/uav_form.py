# ============================================================
# File :        uav_form.py
# Project :     UAV Management Dashboard
# Purpose :     UAV Form Dialog.
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
from app.database.uav_repository import(
	get_companies,
	get_certifications,
	get_uav_statuses,
	create_uav,
	update_uav
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import(
	QAbstractSpinBox,
	QComboBox,
	QDateTimeEdit,
	QDialog,
	QDoubleSpinBox,
	QFormLayout,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QVBoxLayout

)

# ============================================================
#  Form
# ============================================================
class UAVForm(QDialog):
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
		self.serial_number_input = QLineEdit()

		self.company_id_combo = QComboBox()
		self.model_input = QLineEdit()
		self.nickname_input = QLineEdit()

		self.certification_combo = QComboBox()

		self.status_combo = QComboBox()

		self.flight_hours_input = QDoubleSpinBox()
		self.flight_hours_input.setReadOnly(self.mode == "update")
		self.flight_hours_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
		self.flight_hours_input.setDecimals(2)
		self.flight_hours_input.setRange(0.00, 9999.99)
		self.flight_hours_input.setValue(0.00)
		self.flight_hours_input.setSuffix(" hrs")

		self.faa_registration_input = QLineEdit()

		self.issue_date_input = QDateTimeEdit()
		self.issue_date_input.setCalendarPopup(True)
		self.issue_date_input.setDateTime(current)

		self.expiry_date_input = QDateTimeEdit()
		self.expiry_date_input.setCalendarPopup(True)
		self.expiry_date_input.setDateTime(current)


		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("Serial Number", self.serial_number_input)

		form_layout.addRow("Company", self.company_id_combo)
		form_layout.addRow("Model", self.model_input)
		form_layout.addRow("Nickname", self.nickname_input)

		form_layout.addRow("Required Certification", self.certification_combo)

		form_layout.addRow("Status", self.status_combo)
		form_layout.addRow("Flight Hours", self.flight_hours_input)

		form_layout.addRow("FAA Registration", self.faa_registration_input)
		form_layout.addRow("FAA Issued Date", self.issue_date_input)
		form_layout.addRow("FAA Expiry Date", self.expiry_date_input)

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
		self.load_company()
		self.load_certifications()
		self.load_statuses()

		if self.mode == "create":
			self.status_combo.setCurrentText("OPERATIONAL")
			self.status_combo.setEnabled(False)
		else:
			self.status_combo.setEnabled(True)


		# ========================================================
		# Load Existing data
		# ========================================================
		if self.mode == "update":
			self.load_record_data()

	# ========================================================
	# Load Company
	# ======================================================== 
	def load_company(self) -> None:
		try:
			rows = get_companies()

			self.company_id_combo.clear()

			if not rows:
				self.company_id_combo.addItem("No Company Available", None)
				self.company_id_combo.setEnabled(False)
				return

			self.company_id_combo.setEnabled(True)

			for company_id, company_name in rows:
				display_name = company_name

				self.company_id_combo.addItem(display_name, company_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Company Error",str(e))

	# ========================================================
	# Load Certification
	# ======================================================== 
	def load_certifications(self) -> None:
		try:			
			rows = get_certifications()

			self.certification_combo.clear()

			if not rows:
				self.certification_combo.addItem("No Certifications Available", None)
				self.certification_combo.setEnabled(False)
				return

			self.certification_combo.setEnabled(True)

			for certification_id, certification_name in rows:
				display_name = certification_name

				self.certification_combo.addItem(display_name, certification_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Certification Error",str(e))

	# ========================================================
	# Load UAV Status
	# ======================================================== 
	def load_statuses(self) -> None:
		try:
			rows = get_uav_statuses()

			if not rows:
				self.status_combo.addItem("No UAV Status Available",None)
				self.status_combo.setEnabled(False)
				return

			self.status_combo.setEnabled(True)

			for status_id, status_name in rows:
				self.status_combo.addItem(status_name,status_id)

		except Exception as e:
			QMessageBox.critical(self,"Load UAV Status Error",str(e))

	# ========================================================
	# Load Existing Record Data
	# ======================================================== 
	def load_record_data(self) -> None: 
		if not self.record_data:
			return

		self.serial_number_input.setText(self.record_data["asset_serial_number"] or "")

		company_index = self.company_id_combo.findData(self.record_data["asset_company_id"])
		if company_index >= 0:
			self.company_id_combo.setCurrentIndex(company_index)

		self.model_input.setText(self.record_data["asset_model"] or "")
		self.nickname_input.setText(self.record_data["asset_nickname"] or "")

		certification_index = self.certification_combo.findData(self.record_data["asset_cert_id"])
		if certification_index >= 0:
			self.certification_combo.setCurrentIndex(certification_index)

		status_index = self.status_combo.findData(self.record_data["asset_status_id"])
		if status_index >= 0:
			self.status_combo.setCurrentIndex(status_index)

		self.flight_hours_input.setValue(float(self.record_data["asset_flight_hours"] or 0))

		self.faa_registration_input.setText(self.record_data["asset_faa_registration"] or "")
		if self.record_data["asset_issued_date"] is not None:
			self.issue_date_input.setDateTime(self.record_data["asset_issued_date"])
		if self.record_data["asset_expiry_date"] is not None:
			self.expiry_date_input.setDateTime(self.record_data["asset_expiry_date"])

	# ========================================================
	#  Retrieve Form Input Values 
	#  ======================================================== 
	def get_form_data(self) -> dict: 
		return{
			"serial_number": self.serial_number_input.text().strip(),
			"company_id": self.company_id_combo.currentData(),
			"model": self.model_input.text().strip(),
			"nickname": self.nickname_input.text().strip(),
			"certification_id": self.certification_combo.currentData(),
			"status_id": self.status_combo.currentData(),
			"flight_hours": self.flight_hours_input.value(),
			"faa_registration": self.faa_registration_input.text().strip(),
			"issued_date": self.issue_date_input.dateTime().toPyDateTime(),
			"expiry_date": self.expiry_date_input.dateTime().toPyDateTime()
		}

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool: 
		# ====================================================
		# Serial Number
		# ====================================================
		if not form_data["serial_number"]:
			QMessageBox.warning(self,"Validation Error","Please enter a serial number.")
			return False

		# ====================================================
		# Company
		# ====================================================
		if form_data["company_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a company.")
			return False

		# ====================================================
		# Model
		# ====================================================
		if not form_data["model"]:
			QMessageBox.warning(self,"Validation Error","Please enter a UAV model.")
			return False

		# ====================================================
		# Nickname
		# ====================================================
		if not form_data["nickname"]:
			QMessageBox.warning(self,"Validation Error","Please enter a UAV nickname.")
			return False

		# ====================================================
		# Certification
		# ====================================================
		if form_data["certification_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a certification.")
			return False

		# ====================================================
		# Status
		# ====================================================
		if form_data["status_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a status.")
			return False

		# ====================================================
		# Flight Hours
		# ====================================================
		if form_data["flight_hours"] < 0:
			QMessageBox.warning(self,"Validation Error","Flight hours cannot be negative.")
			return False

		# ====================================================
		# FAA Registration
		# ====================================================
		if not form_data["faa_registration"]:
			QMessageBox.warning(self,"Validation Error","Please enter an FAA registration number.")
			return False

		# ====================================================
		# Registration Dates
		# ====================================================
		if form_data["expiry_date"] <= form_data["issued_date"]:
			QMessageBox.warning(self,"Validation Error","Expiry date must be after the issued date.")
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
			create_uav(form_data)

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
			update_uav(self.record_data["asset_id"], form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))
