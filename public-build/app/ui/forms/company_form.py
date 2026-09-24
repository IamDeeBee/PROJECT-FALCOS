# ============================================================
# File :        company_form.py
# Project :     UAV Management Dashboard
# Purpose :     Company Form Dialog.
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
from app.database.company_repository import (
	get_company_statuses,
	create_company,
	update_company
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtWidgets import(
	QComboBox,
	QDialog,
	QFormLayout,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QVBoxLayout

)

# ============================================================
#  Form
# ============================================================
class CompanyForm(QDialog):
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
		self.resize(400,100)
		
		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Field
		# ========================================================
		self.name_input = QLineEdit()
		self.status_combo = QComboBox()

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("Name", self.name_input)
		form_layout.addRow("Status", self.status_combo)

		# ========================================================
		# Populate Status Dopdown
		# ========================================================
		self.load_statuses()

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
		# Load Existing data
		# ========================================================
		if self.mode == "update":
			self.load_record_data()

	# ========================================================
	# Load Company Status
	# ========================================================
	def load_statuses(self) -> None:
		try:
			rows = get_company_statuses()
			
			self.status_combo.clear()
			if not rows:
				self.status_combo.addItem("No Company Status Available",None)
				self.status_combo.setEnabled(False)
				return

			self.status_combo.setEnabled(True)

			for status_id, status_name in rows:
				self.status_combo.addItem(status_name,status_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Company Status Error",str(e))


	# ========================================================
	#  Load Existing Record Data
	#  ======================================================== 
	def load_record_data(self) -> None: 
		if not self.record_data :
			return
		
		self.name_input.setText(self.record_data["company_name"])
		status_index = self.status_combo.findData(self.record_data["company_status_id"])

		if status_index >= 0:
			self.status_combo.setCurrentIndex(status_index)

	# ========================================================
	#  Retrieve Form Input Values 
	#  ======================================================== 
	def get_form_data(self) -> dict: 
		return {
			"name" : self.name_input.text().strip(),
			"status_id" : self.status_combo.currentData()
		}

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool: 
		# ====================================================
		# Name Validation
		# ====================================================
		if not form_data["name"]:
			QMessageBox.warning(self,"Validation Error","Company name cannot be empty.")
			return False

		# ====================================================
		# Status Validation
		# ====================================================
		if form_data["status_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a company status.")
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
			create_company(form_data)

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
			update_company(self.record_data["company_id"], form_data)
						
			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))
