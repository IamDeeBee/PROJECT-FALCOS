# ============================================================
# File :        maintenance_order_form.py
# Project :     UAV Management Dashboard
# Purpose :     Maintenance Order Form Dialog.
#
# Description:
#       Handles:
#           - Creation UI
#           - Update UI
#
# Author :  Debe Okoye
# Created : 2026-07-08
# ============================================================

from app.config.constants import TABLE_MAPPING, FORM_VALID_MODES, MAINTENANCE_TYPE
from app.database.maintenance_order_repository import (
	get_available_uav,
	get_personnel,
	get_maintenance_statuses,
	create_maintenance_order,
	update_maintenance_order
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import(
	QComboBox,
	QDateTimeEdit,
	QDialog,
	QFormLayout,
	QHBoxLayout,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QTextEdit,
	QVBoxLayout
)

# ============================================================
# Maintenance Order Form
# ============================================================
class MaintenanceOrderForm(QDialog):
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
		INPUT_TYPE =("Personnel", "Other")
		
		# ========================================================
		# Window Configuration
		# ========================================================
		self.setWindowTitle(f"{self.mode.title()} {self.table_name}")
		self.resize(500,450)
		
		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Field
		# ========================================================
		self.uav_combo = QComboBox()
		self.maintenance_type_combo = QComboBox()
		self.maintenance_type_combo.addItems(MAINTENANCE_TYPE)
		self.status_combo = QComboBox()

		self.reported_by_type_combo =QComboBox()
		self.reported_by_type_combo.addItems(INPUT_TYPE)

		self.reported_by_internal_combo = QComboBox()
		self.reported_by_internal_combo.setEnabled(False)

		self.refresh_personnel_btn = QPushButton("Refresh")
		self.refresh_personnel_btn.setEnabled(False)

		self.reported_by_external_input = QLineEdit()
		self.reported_by_external_input.setEnabled(False)

		self.reported_date_input = QDateTimeEdit()
		self.reported_date_input.setCalendarPopup(True)
		self.reported_date_input.setDateTime(current)

		self.reason_input = QTextEdit()

		# ========================================================
		# Personnel Layout
		# ========================================================
		personnel_layout = QHBoxLayout()
		personnel_layout.addWidget(self.reported_by_internal_combo)
		personnel_layout.addWidget(self.refresh_personnel_btn)

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("UAV" , self.uav_combo)
		form_layout.addRow("Maintenance Type", self.maintenance_type_combo)
		if self.mode == "update":
			form_layout.addRow("Status" ,self.status_combo)

		form_layout.addRow("Reported By", self.reported_by_type_combo)
		form_layout.addRow("Personnel Name", personnel_layout)
		form_layout.addRow("Name", self.reported_by_external_input)

		form_layout.addRow("Reported Date", self.reported_date_input)
		form_layout.addRow("Reason", self.reason_input)

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
		self.load_available_uav()
		if self.mode == "update":
			self.load_statuses()

		# ========================================================
		# Connect Signals
		# ========================================================
		self.reported_by_type_combo.currentTextChanged.connect(self.toggle_reported_by_fields)
		self.refresh_personnel_btn.clicked.connect(self.load_reported_by)
		self.toggle_reported_by_fields()

		# ========================================================
		# Load Existing data
		# ========================================================
		if self.mode == "update":
			self.load_record_data()

	# ========================================================
	# Toggle "Reported By" Fields
	# ======================================================== 
	def toggle_reported_by_fields(self) -> None:
		# ====================================================
		# Determine Input Type
		# ====================================================
		input_type = self.reported_by_type_combo.currentText()

		# ====================================================
		# Personnel
		# ====================================================
		if input_type == "Personnel":
			self.reported_by_internal_combo.setEnabled(True)
			self.refresh_personnel_btn.setEnabled(True)
			self.reported_by_external_input.setEnabled(False)

			self.reported_by_external_input.clear()

			if self.reported_by_internal_combo.count() == 0:
				self.load_reported_by()

		# ====================================================
		# Other
		# ====================================================
		else:
			self.reported_by_internal_combo.setEnabled(False)
			self.reported_by_internal_combo.setCurrentIndex(-1)
			self.refresh_personnel_btn.setEnabled(False)

			self.reported_by_external_input.setEnabled(True)

			self.reported_by_external_input.style().unpolish(self.reported_by_external_input)
			self.reported_by_external_input.style().polish(self.reported_by_external_input) 

	# ========================================================
	# Load Available UAV
	# ========================================================
	def load_available_uav(self) -> None:
		try:
			rows = get_available_uav()

			self.uav_combo.clear()

			if not rows:
				self.uav_combo.addItem("No UAVs Available for Maintenance", None)
				self.uav_combo.setEnabled(False)
				return
			
			self.uav_combo.setEnabled(True)

			for asset_id, asset_nickname in rows:
				display_name = asset_nickname
				self.uav_combo.addItem(display_name, asset_id)

		except Exception as e:
			QMessageBox.critical(self,"Load UAV Error",str(e))
				

	# ========================================================
	# Load Personnel
	# ========================================================
	def load_reported_by(self) -> None:
		try:
			rows = get_personnel()

			self.reported_by_internal_combo.clear()

			if not rows:
				self.reported_by_internal_combo.addItem("No Personnel Available", None)
				self.reported_by_internal_combo.setEnabled(False)
				return
			
			self.reported_by_internal_combo.setEnabled(True)

			for person_id, first_name, last_name, email in rows:
				if email:
					display_name = (f"{first_name} {last_name} ({email})")
				else:
					display_name = (f"{first_name} {last_name}")
				self.reported_by_internal_combo.addItem(display_name,person_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Personnel Error",str(e))

		
	# ========================================================
	# Load Maintenance Status
	# ======================================================== 
	def load_statuses(self) -> None:
		try:
			rows = get_maintenance_statuses()

			self.status_combo.clear()

			if not rows:
				self.status_combo.addItem("No Maintenance Status Available",None)
				self.status_combo.setEnabled(False)
				return

			self.status_combo.setEnabled(True)

			for status_id, status_name in rows:
				self.status_combo.addItem(status_name,status_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Maintenance Status Error",str(e))

		
	# ========================================================
	# Load Existing Record Data
	# ======================================================== 
	def load_record_data(self) -> None:
		if not self.record_data:
			return
		
		uav_index = self.uav_combo.findData(self.record_data["maint_asset_id"])
		if uav_index >= 0:
			self.uav_combo.setCurrentIndex(uav_index)

		self.maintenance_type_combo.setCurrentText(self.record_data["maint_type"])

		status_index = self.status_combo.findData(self.record_data["maint_status_id"])
		if status_index >= 0:
			self.status_combo.setCurrentIndex(status_index)

		if self.record_data["maint_reported_by_person_id"] is not None:
			self.reported_by_type_combo.setCurrentText("Personnel")
			person_index = self.reported_by_internal_combo.findData(self.record_data["maint_reported_by_person_id"])
			if person_index >= 0:
				self.reported_by_internal_combo.setCurrentIndex(person_index)
		else:
			self.reported_by_type_combo.setCurrentText("Other")
			self.reported_by_external_input.setText(self.record_data["maint_reported_by_external_name"])

		if self.record_data["maint_reported_date"] is not None:
			self.reported_date_input.setDateTime(self.record_data["maint_reported_date"])
		
		self.reason_input.setPlainText(self.record_data["maint_reason"])

	# ========================================================
	# Retrieve Form Input Values 
	# ======================================================== 
	def get_form_data(self) -> dict: 
		return{
			"asset_id": self.uav_combo.currentData(),
			"maintenance_type": self.maintenance_type_combo.currentText(),
			"status_id": self.status_combo.currentData(),
			"reported_by_person_id": self.reported_by_internal_combo.currentData(),
			"reported_by_external_name": self.reported_by_external_input.text().strip() or None,
			"reported_date": self.reported_date_input.dateTime().toPyDateTime(),
			"reason": self.reason_input.toPlainText().strip()
		}

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool:
		# ====================================================
		# UAV
		# ====================================================
		if form_data["asset_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a UAV.")
			return False

		# ====================================================
		# Reported By
		# ====================================================
		if form_data["reported_by_person_id"] is None and not form_data["reported_by_external_name"]:
			QMessageBox.warning(self,"Validation Error","Please specify who reported the maintenance.")
			return False

		# ====================================================
		# Maintenance Reason
		# ====================================================
		if not form_data["reason"]:
			QMessageBox.warning(self,"Validation Error","Maintenance reason cannot be empty.")
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
			create_maintenance_order(form_data)

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
			update_maintenance_order(self.record_data["maint_id"],form_data)
			
			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))

		