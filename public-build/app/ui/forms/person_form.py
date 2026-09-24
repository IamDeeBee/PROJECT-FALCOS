# ============================================================
# File :        person_form.py
# Project :     UAV Management Dashboard
# Purpose :     Person Form Dialog.
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

from app.database.person_repository import (
	create_person,
	update_person
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtWidgets import(
	QDialog,
	QFormLayout,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QVBoxLayout

)

# ============================================================
# Person Form
# ============================================================
class PersonForm(QDialog):
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
		self.resize(400,150)
		
		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Field
		# ========================================================
		self.first_name_input= QLineEdit()
		self.last_name_input= QLineEdit()
		self.primary_email_input= QLineEdit()

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("First Name", self.first_name_input)
		form_layout.addRow("Last Name", self.last_name_input)
		form_layout.addRow("Email", self.primary_email_input)

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
	#  Load Existing Record Data
	#  ======================================================== 
	def load_record_data(self) -> None: 
		if not self.record_data:
			return
		
		self.first_name_input.setText(self.record_data["person_first_name"])
		self.last_name_input.setText(self.record_data["person_last_name"])
		self.primary_email_input.setText(self.record_data["person_primary_email"])

	# ========================================================
	#  Retrieve Form Input Values 
	#  ======================================================== 
	def get_form_data(self) -> dict:
		return {
			"first_name" : self.first_name_input.text().strip(),
			"last_name" : self.last_name_input.text().strip(),
			"primary_email" : self.primary_email_input.text().strip()
		} 

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool: 
		# ========================================================
		# First Name Validation
		# ========================================================
		if not form_data["first_name"]:
			QMessageBox.warning(self,"Validation Error","First name cannot be empty.")
			return False
		
		# ========================================================
		# Last Name Validation
		# ========================================================
		if not form_data["last_name"]:
			QMessageBox.warning(self,"Validation Error","Last name cannot be empty.")
			return False
		
		# ========================================================
		# Email Validation
		# ========================================================
		if "@" not in form_data["primary_email"]:
			QMessageBox.warning(self,"Validation Error","Please Enter Email.")
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
			create_person(form_data)

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
			update_person(self.record_data["person_id"],form_data)
		
			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))
