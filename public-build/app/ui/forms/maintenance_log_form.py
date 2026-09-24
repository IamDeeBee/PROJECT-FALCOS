# ============================================================
# File :        maintenance_log_form.py
# Project :     UAV Management Dashboard
# Purpose :     Maintenance Log Form Dialog.
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
from app.database.maintenance_log_repository import (
	get_reported_maintenance_orders,
	get_all_maintenance_orders,
	get_maintenance_order_details,
	get_maintenance_statuses,
	get_technicians,
	create_maintenance_log,
	update_maintenance_log
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
#  Maintenance Log Form
# ============================================================
class MaintenanceLogForm(QDialog):
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
		INPUT_TYPE =("Technician", "Other")
		
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
		self.maintenance_combo =QComboBox()

		self.uav_input = QLineEdit()
		self.uav_input.setReadOnly(True)

		self.maintenance_type_input = QLineEdit()
		self.maintenance_type_input.setReadOnly(True)

		self.reported_by_input = QLineEdit()
		self.reported_by_input.setReadOnly(True)

		self.reason_input = QTextEdit()
		self.reason_input.setReadOnly(True)

		self.status_combo = QComboBox()

		self.maintenance_start_date_input = QDateTimeEdit()
		self.maintenance_start_date_input.setCalendarPopup(True)
		self.maintenance_start_date_input.setDateTime(current)

		self.maintenance_completed_date_input = QDateTimeEdit()
		self.maintenance_completed_date_input.setCalendarPopup(True)
		self.maintenance_completed_date_input.setDateTime(current)
		
		self.performed_by_type_combo =QComboBox()
		self.performed_by_type_combo.addItems(INPUT_TYPE)

		self.performed_by_internal_combo = QComboBox()
		self.performed_by_internal_combo.setEnabled(False)

		self.refresh_technician_btn = QPushButton("Refresh")
		self.refresh_technician_btn.setEnabled(False)

		self.performed_by_external_input = QLineEdit()
		self.performed_by_external_input.setEnabled(False)

		self.description_input = QTextEdit()

		self.note_input = QTextEdit()

		# ========================================================
		# Technician Layout
		# ========================================================
		technician_layout = QHBoxLayout()
		technician_layout.addWidget(self.performed_by_internal_combo)
		technician_layout.addWidget(self.refresh_technician_btn)

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("Maintenance Order", self.maintenance_combo)

		form_layout.addRow("UAV", self.uav_input)
		form_layout.addRow("Maintenance Type", self.maintenance_type_input)
		form_layout.addRow("Reported By", self.reported_by_input)
		form_layout.addRow("Reason", self.reason_input)

		form_layout.addRow("Status", self.status_combo)

		form_layout.addRow("Started Date", self.maintenance_start_date_input)
		form_layout.addRow("Completed Date", self.maintenance_completed_date_input)

		form_layout.addRow("Performed By", self.performed_by_type_combo)
		form_layout.addRow("Technician", technician_layout)
		form_layout.addRow("Name", self.performed_by_external_input)

		form_layout.addRow("Description", self.description_input)
		form_layout.addRow("Notes", self.note_input)

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
			self.load_reported_maintenance_orders()
		else:
			self.load_all_maintenance_orders()

		self.load_statuses()

		# ========================================================
		# Connect Signals
		# ========================================================
		self.maintenance_combo.currentIndexChanged.connect(self.populate_maintenance_details)
		self.populate_maintenance_details()
		self.performed_by_type_combo.currentTextChanged.connect(self.toggle_performed_by_fields)
		self.refresh_technician_btn.clicked.connect(self.load_performed_by)
		self.toggle_performed_by_fields()

		# ========================================================
		# Load Existing data
		# ========================================================
		if self.mode == "update":
			self.maintenance_combo.setEnabled(False)
			self.load_record_data()

	# ========================================================
	# Load Open Maintenance Order
	# ======================================================== 
	def load_reported_maintenance_orders(self) -> None:
	
		try:
			rows = get_reported_maintenance_orders()

			self. maintenance_combo.clear()

			if not rows:
				self. maintenance_combo.addItem("No Reported Maintenance Orders",None)
				self. maintenance_combo.setEnabled(False)
				return

			self. maintenance_combo.setEnabled(True)

			for maint_id, asset_name, maint_type, reported_date in rows:
				display_name = (
					f"#{maint_id} | "
					f"{asset_name} | "
					f"{maint_type} | "
					f"{reported_date:%Y-%m-%d %H:%M}"
				)

				self. maintenance_combo.addItem(display_name, maint_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Maintenance Order Error",str(e))

	
	# ========================================================
	# Load All Maintenance Order
	# ======================================================== 
	def load_all_maintenance_orders(self) -> None:
		try:
			rows = get_all_maintenance_orders()

			self. maintenance_combo.clear()

			if not rows:
				self. maintenance_combo.addItem("No Maintenance Orders",None)
				self. maintenance_combo.setEnabled(False)
				return

			self. maintenance_combo.setEnabled(True)

			for maint_id, asset_name, maint_type, reported_date in rows:
				display_name = (
					f"#{maint_id} | "
					f"{asset_name} | "
					f"{maint_type} | "
					f"{reported_date:%Y-%m-%d %H:%M}"
				)

				self. maintenance_combo.addItem(display_name, maint_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Maintenance Order Error",str(e))

	# ========================================================
	# Populate Maintenance Details
	# ======================================================== 
	def populate_maintenance_details(self) -> None: 
		maint_id = self.maintenance_combo.currentData()
		
		if maint_id is None:
			self.clear_maintenance_details()
			return
		
		try:
						
			row = get_maintenance_order_details(maint_id)

			if row:
				(
					asset_nickname,
					maintenance_type,
					reported_by,
					reason,
					status_id
				) = row

				self.uav_input.setText(asset_nickname)
				self.maintenance_type_input.setText(maintenance_type)
				self.reported_by_input.setText(reported_by)
				self.reason_input.setPlainText(reason)

				status_index = self.status_combo.findData(status_id)
				if status_index >= 0:
					self.status_combo.setCurrentIndex(status_index)

		except Exception as e:
			QMessageBox.critical(self, "Maintenance Error", str(e))

	# ========================================================
	# Clear Maintenance Details
	# ======================================================== 
	def clear_maintenance_details(self) -> None:
		self.uav_input.clear()
		self.maintenance_type_input.clear()
		self.reported_by_input.clear()
		self.reason_input.clear()
		self.status_combo.setCurrentIndex(-1)

	# ========================================================
	# Toggle "Performed By" Fields
	# ======================================================== 
	def toggle_performed_by_fields(self) -> None: 
		# ====================================================
		# Determine Input Type
		# ====================================================
		input_type = self.performed_by_type_combo.currentText()

		# ====================================================
		# Technician
		# ====================================================
		if input_type == "Technician":
			self.performed_by_internal_combo.setEnabled(True)

			self.refresh_technician_btn.setEnabled(True)

			self.performed_by_external_input.setEnabled(False)
			self.performed_by_external_input.clear()

			if self.performed_by_internal_combo.count() == 0:
				self.load_performed_by()


		# ====================================================
		# Other
		# ====================================================
		else:
			self.performed_by_internal_combo.setEnabled(False)
			self.performed_by_internal_combo.setCurrentIndex(-1)

			self.refresh_technician_btn.setEnabled(False)

			self.performed_by_external_input.setEnabled(True)
			self.performed_by_external_input.style().unpolish(self.performed_by_external_input)
			self.performed_by_external_input.style().polish(self.performed_by_external_input)

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
	# Load Technicians
	# ======================================================== 
	def load_performed_by(self) -> None:
		try:
			rows = get_technicians()

			self.performed_by_internal_combo.clear()

			if not rows:
				self.performed_by_internal_combo.addItem("No Technician Available", None)
				self.performed_by_internal_combo.setEnabled(False)
				return
			
			self.performed_by_internal_combo.setEnabled(True)

			for technician_id, first_name, last_name, email in rows:
				if email:
					display_name = f"{first_name} {last_name} ({email})"
				else:
					display_name = f"{first_name} {last_name}"
				self.performed_by_internal_combo.addItem(display_name,technician_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Technician Error",str(e))

	# ========================================================
	# Load Existing Record Data
	# ======================================================== 
	def load_record_data(self) -> None: 
		if not self.record_data :
			return
		
		maintenance_index = self.maintenance_combo.findData(self.record_data["maint_id"])
		if maintenance_index >= 0:
			self.maintenance_combo.setCurrentIndex(maintenance_index)

		status_index = self.status_combo.findData(self.record_data["maint_status_id"])
		if status_index >= 0:
			self.status_combo.setCurrentIndex(status_index)

		if self.record_data["maint_started_date"] is not None:
			self.maintenance_start_date_input.setDateTime(self.record_data["maint_started_date"])
		if self.record_data["maint_completed_date"] is not None:
			self.maintenance_completed_date_input.setDateTime(self.record_data["maint_completed_date"])

		if self.record_data["maint_performed_by_technician_id"] is not None:
			self.performed_by_type_combo.setCurrentText("Technician")
			technician_index = self.performed_by_internal_combo.findData(self.record_data["maint_performed_by_technician_id"])
			if technician_index >= 0:
				self.performed_by_internal_combo.setCurrentIndex(technician_index)
		else:
			self.performed_by_type_combo.setCurrentText("Other")
			self.performed_by_external_input.setText(self.record_data["maint_performed_by_external_name"])
		
		self.description_input.setPlainText(self.record_data["maint_description"])
		self.note_input.setPlainText(self.record_data["maint_notes"])

	
	# ========================================================
	# Retrieve Form Input Values 
	# ======================================================== 
	def get_form_data(self) -> dict: 
		return {
			"maint_id": self.maintenance_combo.currentData(),
			"status_id": self.status_combo.currentData(),
			"started_date": self.maintenance_start_date_input.dateTime().toPyDateTime(),
			"completed_date": self.maintenance_completed_date_input.dateTime().toPyDateTime(),
			"performed_by_technician_id": self.performed_by_internal_combo.currentData(),
			"performed_by_external_name": self.performed_by_external_input.text().strip() or None,
			"description": self.description_input.toPlainText().strip() or None,
			"note": self.note_input.toPlainText().strip() or None
		}
	
	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool: 
		# ====================================================
		# Maintenance Record
		# ====================================================
		if form_data["maint_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a maintenance order.")
			return False

		# ====================================================
		# Performed By
		# ====================================================
		if self.performed_by_type_combo.currentText() == "Technician":
			if form_data["performed_by_technician_id"] is None:
				QMessageBox.warning(self,"Validation Error","Please select a technician.")
				return False
		else:
			if not form_data["performed_by_external_name"]:
				QMessageBox.warning(self,"Validation Error","Please enter the technician's name.")
				return False

		# ====================================================
		# Maintenance Dates
		# ====================================================
		if form_data["completed_date"] < form_data["started_date"]:
			QMessageBox.warning(self,"Validation Error","Completed date cannot be earlier than the started date.")
			return False

		# ====================================================
		# Description
		# ====================================================
		if not form_data["description"]:
			QMessageBox.warning(self,"Validation Error","Maintenance description cannot be empty.")
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

			create_maintenance_log(form_data)

			refresh_monitor_table(self.window)

			# ====================================================
			# Activity Feed
			# ====================================================
			self.window.log_activity(
				f"Created {self.table_name}"
			)

			# ====================================================
			# Success Message
			# ====================================================
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
			update_maintenance_log(form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))
