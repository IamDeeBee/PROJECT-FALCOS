# ============================================================
# File :        certification_form.py
# Project :     UAV Management Dashboard
# Purpose :     Certification Form Dialog.
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
from app.database.certification_repository import (
	create_certification,
	update_certification
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
# Certification Form
# ============================================================
class CertificationForm(QDialog):
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
		if self.mode =="create":
			self.resize(400,150)
		else:
			self.resize(400,150)
		
		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Field
		# ========================================================
		self.name_input = QLineEdit()
		self.provider_input = QLineEdit()
		self.provider_website_input = QLineEdit()

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("Name", self.name_input)
		form_layout.addRow("Provider", self.provider_input)
		form_layout.addRow("Website", self.provider_website_input)

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
		
		self.name_input.setText(self.record_data["cert_name"])
		self.provider_input.setText(self.record_data["cert_provider"])
		self.provider_website_input.setText(self.record_data["cert_provider_website"] or "")

	# ========================================================
	#  Retrieve Form Input Values 
	#  ======================================================== 
	def get_form_data(self) -> dict:
		return {
			"name" : self.name_input.text().strip(),
			"provider" : self.provider_input.text().strip(),
			"provider_website" : self.provider_website_input.text().strip()
		}

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool:
		# ========================================================
		# Name Validation
		# ========================================================
		if not form_data["name"]:
			QMessageBox.warning(self,"Validation Error","Certification name cannot be empty.")
			return False

		# ========================================================
		# Provider Validation
		# ========================================================
		if not form_data["provider"]:
			QMessageBox.warning(self,"Validation Error","Certification provider cannot be empty.")
			return False

		# ========================================================
		# Optional Fields
		# ========================================================
		if form_data["provider_website"] == "":
			form_data["provider_website"] = None
		
		return True

	# ========================================================  
	# Creation Logic  
	# ========================================================
	def create_entry(self) -> None:
		form_data = self.get_form_data()

		if not self.validate_form_data(form_data):
			return

		try:
			create_certification(form_data)			

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Created {self.table_name} record"
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
			update_certification(self.record_data["cert_id"], form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))