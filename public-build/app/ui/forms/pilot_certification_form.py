# ============================================================
# File :        pilot_certification_form.py
# Project :     UAV Management Dashboard
# Purpose :     Pilot Certification Form Dialog.
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
from app.database.pilot_certification_repository import(
	get_certifications,
	get_active_pilots,
	create_pilot_certification,
	update_pilot_certification,
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import(
	QComboBox,
	QDateEdit,
	QDialog,
	QFormLayout,
	QHBoxLayout,
	QLineEdit,
	QMessageBox,
	QPushButton,
	QVBoxLayout

)

# ============================================================
# Pilot Certification Form
# ============================================================
class PilotCertificationForm(QDialog):
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
		current = QDate.currentDate()
		CERTIFICATION_APPROVAL = ('PENDING_APPROVAL','APPROVED','REJECTED')
		CERTIFICATION_VALIDITY = ('ACTIVE','EXPIRING_90_DAYS','EXPIRING_30_DAYS','EXPIRED')

		# ========================================================
		# Window Configuration
		# ========================================================
		self.setWindowTitle(f"{self.mode.title()} {self.table_name}")
		if self.mode == "update":
			self.resize(450,325)
		else:
			self.resize(450,150)
		
		# ========================================================
		# Main layout
		# ========================================================
		layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		# ========================================================
		# Input Field
		# ========================================================
		self.certification_combo = QComboBox()

		self.refresh_certification_btn = QPushButton("Refresh")

		self.pilot_combo = QComboBox()

		self.refresh_pilot_btn = QPushButton("Refresh")
		
		self.certification_number_input = QLineEdit()

		self.approval_status_combo = QComboBox()
		self.approval_status_combo.addItems(CERTIFICATION_APPROVAL)
		self.approval_status_combo.setEnabled(False if self.mode == "create" else True)

		self.validity_status_combo = QComboBox()
		self.validity_status_combo.addItems(CERTIFICATION_VALIDITY)

		self.issue_date_input = QDateEdit()
		self.issue_date_input.setCalendarPopup(True)
		self.issue_date_input.setDate(current)

		self.expiry_date_input = QDateEdit()
		self.expiry_date_input.setCalendarPopup(True)
		self.expiry_date_input.setDate(current)

		# ========================================================
		# Certification & Pilot Refresh Layout
		# ========================================================
		certification_layout = QHBoxLayout()
		certification_layout.addWidget(self.certification_combo)
		certification_layout.addWidget(self.refresh_certification_btn)

		pilot_layout = QHBoxLayout()
		pilot_layout.addWidget(self.pilot_combo)
		pilot_layout.addWidget(self.refresh_pilot_btn)

		# ========================================================
		# Form Rows
		# ========================================================
		form_layout.addRow("Certification",certification_layout)
		form_layout.addRow("Pilot",pilot_layout)
		form_layout.addRow("Certification Number",self.certification_number_input)
		form_layout.addRow("Approval Status",self.approval_status_combo)
		if self.mode == "update":
			form_layout.addRow("Validity Status",self.validity_status_combo)
		form_layout.addRow("Issue Date",self.issue_date_input)
		form_layout.addRow("Expiry Date",self.expiry_date_input)

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
		# Populate Combo Boxes
		# ========================================================
		self.load_certifications()
		self.load_pilots() 

		# ========================================================
		# Connect Signals
		# ========================================================
		self.refresh_certification_btn.clicked.connect(self.load_certifications)
		self.refresh_pilot_btn.clicked.connect(self.load_pilots)
		
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
	# Populate Certification
	# ======================================================== 
	def load_certifications(self) -> None:
		try:
			rows = get_certifications()

			self.certification_combo.clear()

			if not rows:
				self.certification_combo.addItem("No Certifications Available",None)
				self.certification_combo.setEnabled(False)
				return

			self.certification_combo.setEnabled(True)

			for cert_id, cert_name in rows:
				self.certification_combo.addItem(cert_name,cert_id)

		except Exception as e:
			QMessageBox.critical(self,"Load Certification Error",str(e))

	# ========================================================
	# Populate Pilot
	# ======================================================== 
	def load_pilots(self) -> None: 
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
	#  Load Existing Record Data
	#  ======================================================== 
	def load_record_data(self) -> None:  
		if not self.record_data:
			return

		certification_index = self.certification_combo.findData(self.record_data["pilcert_cert_id"])
		if certification_index >= 0:
			self.certification_combo.setCurrentIndex(certification_index)

		pilot_index = self.pilot_combo.findData(self.record_data["pilcert_pilot_id"])
		if pilot_index >= 0:
			self.pilot_combo.setCurrentIndex(pilot_index)

		self.certification_number_input.setText(self.record_data["pilcert_certification_number"] or "")
		self.approval_status_combo.setCurrentText(self.record_data["pilcert_approval_status"])
		self.validity_status_combo.setCurrentText(self.record_data["pilcert_validity_status"])
	
		if self.record_data["pilcert_issue_date"] is not None:
			self.issue_date_input.setDate(self.record_data["pilcert_issue_date"])
		if self.record_data["pilcert_expiry_date"] is not None:
			self.expiry_date_input.setDate(self.record_data["pilcert_expiry_date"])

	# ========================================================
	#  Retrieve Form Input Values 
	#  ======================================================== 
	def get_form_data(self) -> dict:
		return {
			"certification_id": self.certification_combo.currentData(),
			"pilot_id": self.pilot_combo.currentData(),
			"certification_number": self.certification_number_input.text().strip() or None,
			"approval_status": self.approval_status_combo.currentText(),
			"issue_date": self.issue_date_input.date().toPyDate(),
			"expiry_date": self.expiry_date_input.date().toPyDate()
		}

	# ======================================================== 
	# Validate Form Data 
	# ======================================================== 
	def validate_form_data( self, form_data: dict ) -> bool:
		# ====================================================
		# Certification
		# ====================================================
		if form_data["certification_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a certification.")
			return False

		# ====================================================
		# Pilot
		# ====================================================
		if form_data["pilot_id"] is None:
			QMessageBox.warning(self,"Validation Error","Please select a pilot.")
			return False

		# ====================================================
		# Certification Number
		# ====================================================
		# Optional field
		# No validation required

		# ====================================================
		# Approval Status
		# ====================================================
		if not form_data["approval_status"]:
			QMessageBox.warning(self,"Validation Error","Please select an approval status.")
			return False

		# ====================================================
		# Certification Dates
		# ====================================================
		if form_data["expiry_date"] < form_data["issue_date"]:
			QMessageBox.warning(self,"Validation Error","Expiry date cannot be earlier than the issue date.")
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
			create_pilot_certification(form_data)

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
			update_pilot_certification(self.record_data["pilcert_id"],form_data)

			refresh_monitor_table(self.window)

			self.window.log_activity(
				f"Updated {self.table_name}"
			)

			QMessageBox.information(self,"Success",f"{self.table_name} updated successfully.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Update Error",str(e))
