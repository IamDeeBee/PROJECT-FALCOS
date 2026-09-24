# ============================================================
# File:         search_dialog.py
# Project:      UAV Management Dashboard
# Purpose:      Search dialog window.
#
# Description:
#       Handles:
#           - PostgreSQL search queries
#           - displaying matching records depending on the button clicked
#
# Author: Debe Okoye
# Created: 2026-06-08
# ============================================================
from app.config.constants import SEARCH_DIALOG_MAPPING, DB_SCHEMA, TABLE_MAPPING
from app.database.search_repository import (
	search_records,
	get_record,
	delete_record
)
from app.ui.monitor import refresh_monitor_table
from PyQt6.QtWidgets import(
QDialog,
QHBoxLayout,
QLabel,
QLineEdit,
QMessageBox,
QPushButton,
QTableWidget,
QTableWidgetItem,
QVBoxLayout
)

# ============================================================
# Search Dialog
# ============================================================

class SearchDialog(QDialog):
	def __init__(self, window, table_name, mode="update"):
		super().__init__()
		self.window = window
		self.table_name = table_name
		self.selected_record = None
		self.mode = mode

		# Window Configuration
		if self.mode == "delete":
			self.setWindowTitle(f"Delete {self.table_name}")
		else :
			self.setWindowTitle(f"{self.table_name} Search")
		self.resize(900, 500)

		# Main Layout
		layout = QVBoxLayout(self)

		# Search Row
		search_row = QHBoxLayout()

		search_info = SEARCH_DIALOG_MAPPING[self.table_name]
		search_label = QLabel(f"{search_info['search_label']}:")
		self.search_input = QLineEdit()

		search_btn = QPushButton("Search")
		search_btn.clicked.connect(self.search_table)

		search_row.addWidget(search_label)
		search_row.addWidget(self.search_input)
		search_row.addWidget(search_btn)

		# Select Button
		select_btn = QPushButton(f"Select {self.table_name}" if self.mode == "update" else f"Delete {self.table_name}")

		if self.mode == "delete":
			select_btn.clicked.connect(self.delete_item)
		else :
			select_btn.clicked.connect(self.select_item)
		

		# Results Table
		self.results_table = QTableWidget()
		self.results_table.verticalHeader().setVisible(False)

		# Organize Layout
		layout.addLayout(search_row)
		layout.addWidget(self.results_table)
		layout.addWidget(select_btn)

	# ============================================================
	# Search Table Records
	# ============================================================
	def search_table(self) -> None:
		search_info = SEARCH_DIALOG_MAPPING[self.table_name]
		search_column = search_info["search_column"]
		db_view = search_info["view"]
		search_label = search_info["search_label"]

		try:
			# Retrieve Search Input
			search_input = (self.search_input.text().strip())

			# Validation
			if not search_input:
				search_info = SEARCH_DIALOG_MAPPING[self.table_name]
				QMessageBox.warning(self,"Search Error",f"{search_label} cannot be empty.")
				return

			column_names, rows = search_records(db_view, search_column, search_input)

			# Configure Results Table
			self.results_table.setColumnCount(len(column_names))
			self.results_table.setHorizontalHeaderLabels(column_names)
			self.results_table.setRowCount(len(rows))

			# Populate Results Table
			for row_idx, row_data in enumerate(rows):
				for col_idx, value in enumerate(row_data):
					self.results_table.setItem(row_idx,col_idx,QTableWidgetItem(str(value)))

		except Exception as e:
			QMessageBox.critical(self,"Search Error",str(e))

	# ============================================================
	# Select  Record
	# ============================================================
	def select_item(self) -> None:

		selected_row = (self.results_table.currentRow())

		if selected_row < 0:
			QMessageBox.warning(self,"Selection Error","Please select a record.")
			return

		# --------------------------------------------------------
		# Retrieve Search Information
		# --------------------------------------------------------
		search_info = SEARCH_DIALOG_MAPPING[self.table_name]
		table = search_info["table"]
		primary_key = search_info["primary_key"]

		# --------------------------------------------------------
		# Retrieve Selected Record ID
		# --------------------------------------------------------
		record_id = None

		for column in range(self.results_table.columnCount()):
			header = self.results_table.horizontalHeaderItem(column).text()

			if header.lower() == "id":
				item = self.results_table.item(selected_row, column)
				record_id = item.text() if item else None
				break

		if record_id is None:
			QMessageBox.warning(
				self,
				"Selection Error",
				"Unable to determine the selected record."
			)
			return

		# --------------------------------------------------------
		# Retrieve Full Record From Database
		# --------------------------------------------------------
		record = get_record(table, primary_key, record_id)

		if record is None:
			QMessageBox.warning(
				self,
				"Database Error",
				"Selected record no longer exists."
			)

			return

		self.selected_record = dict(record)
		self.accept()


	# ============================================================
	# Delete  Record
	# ============================================================
	def delete_item(self) -> None:
		selected_row = (self.results_table.currentRow())

		if selected_row < 0:
			QMessageBox.warning(self,"Selection Error","Please select a record.")
			return

		record_id_item = (self.results_table.item(selected_row,0))
		record_id = record_id_item.text()

		table_name = TABLE_MAPPING[self.table_name]
		search_info = SEARCH_DIALOG_MAPPING[self.table_name]
		primary_key = search_info["primary_key"]

		confirm = QMessageBox.question(
			self,
			"Confirm Delete",
			(
				f"Delete record "
				f"(ID: {record_id})?"
			)
		)
		if confirm != QMessageBox.StandardButton.Yes:
			return

		try:
			delete_record(table_name, primary_key, record_id)

			QMessageBox.information(self,"Delete Success","Record deleted successfully.")

			refresh_monitor_table(self.window)

			self.window.log_activity(f"Deleted {self.table_name} record.")
			self.accept()

		except Exception as e:
			QMessageBox.critical(self,"Delete Error",str(e))

