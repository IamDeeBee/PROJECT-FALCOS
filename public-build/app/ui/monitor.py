# ============================================================
# File:         monitor.py
# Project:      UAV Management Dashboard
# Purpose:      Monitor tab construction and table monitoring
#               functionality.
#
# Description:
#       Handles:
#       - monitor tab layout
#       - refresh system
#       - dynamic table viewing
#       - monitor table population
#
# Author: Debe Okoye
# Created: 2026-06-02
# ============================================================
from app.database.monitor_repository import get_monitor_data
from PyQt6.QtCore import (
	Qt,
	QPoint
)
from PyQt6.QtWidgets import (
	QAbstractItemView,
	QHBoxLayout,
	QHeaderView,
	QLabel,
	QMenu,
	QPushButton,
	QTableWidget,
	QTableWidgetItem,
	QVBoxLayout,
	QWidget
)
# ============================================================
# Filterable Table Header
# ============================================================
class FilterableHeader(QHeaderView):

	def __init__(self, orientation, table):
		super().__init__(orientation, table)

		self.table = table

		self.setSectionsClickable(True)
		self.sectionClicked.connect(self.show_filter_menu)

	# ========================================================
	# Show Filter Menu
	# ========================================================
	def show_filter_menu(self, column_index):
		table = self.table

		menu = QMenu(self)

		# ========================================================
		# Show All Option
		# ========================================================
		show_all_action = menu.addAction("All")
		show_all_action.triggered.connect(
			lambda: self.filter_column(column_index, None)
		)

		menu.addSeparator()

		# ========================================================
		# Retrieve Unique Column Values
		# ========================================================
		values = set()

		for row in range(table.rowCount()):
			item = table.item(row, column_index)

			if item:
				values.add(item.text())

		# ========================================================
		# Create Filter Options
		# ========================================================
		for value in sorted(values):
			action = menu.addAction(value)
			action.triggered.connect(
				lambda checked=False, value=value:
					self.filter_column(column_index, value)
			)

		menu.exec(
			self.mapToGlobal(
				QPoint(self.sectionPosition(column_index), self.height()) 
			)
		)

	# ============================================================
	# Filter Table Column
	# ============================================================
	def filter_column(self, column_index, value):
		table = self.table

		for row in range(table.rowCount()):

			item = table.item(row, column_index)

			if value is None:
				table.setRowHidden(row, False)

			else:
				if item and item.text() == value:
					table.setRowHidden(row, False)
				else:
					table.setRowHidden(row, True)

# ============================================================
# Monitor Page Construction
# ============================================================
def build_monitor_page(window) -> QWidget:
	page = QWidget()

	layout = QVBoxLayout(page)

	top_bar = QHBoxLayout()

	window.monitor_label = QLabel("No table selected")

	refresh_btn = QPushButton("Refresh")
	refresh_btn.clicked.connect(lambda: refresh_monitor_table(window))

	top_bar.addWidget(window.monitor_label)
	top_bar.addStretch()
	top_bar.addWidget(refresh_btn)

	window.monitor_table = QTableWidget()
	window.monitor_table.verticalHeader().setVisible(False)
	

	layout.addLayout(top_bar)
	layout.addWidget(window.monitor_table)

	return page

# ============================================================
# Monitor Table Loader
# ============================================================
def load_monitor_table(window, table_name: str, db_view: str) -> None:
	window.current_disp_table = table_name
	window.current_db_table = db_view


	window.monitor_label.setText(f"Viewing: {table_name}")

	rows, column_names = get_monitor_data(db_view)

	window.monitor_table.setColumnCount(len(column_names))
	window.monitor_table.setRowCount(len(rows))



	window.monitor_table.setHorizontalHeader(
		FilterableHeader(Qt.Orientation.Horizontal, window.monitor_table)
	)

	window.monitor_table.horizontalHeader().setVisible(True)
	window.monitor_table.setHorizontalHeaderLabels(column_names)
	window.monitor_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
	window.monitor_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
	window.monitor_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
	
	for row_idx, row_data in enumerate(rows):
		for col_idx, value in enumerate(row_data):
			window.monitor_table.setItem(row_idx,col_idx,QTableWidgetItem(str(value)))

	window.monitor_table.resizeColumnsToContents()
	window.log_activity(f"Loaded {table_name} table.")

	

# ============================================================
# Monitor Refresh Logic
# ============================================================
def refresh_monitor_table(window) -> None:

	# Reloads Current Monitor Table
	if (hasattr(window, "current_disp_table")and hasattr(window, "current_db_table")):
		load_monitor_table(window,window.current_disp_table,window.current_db_table)
