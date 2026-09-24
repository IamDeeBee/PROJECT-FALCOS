# ============================================================
# File:         sidebar.py
# Project:      UAV Management Dashboard
# Purpose:      Sidebar construction and CRUD navigation logic.


# Description:
#       Handles:
#       - sidebar layout
#       - CRUD toolbox creation
#       - table operation routing
#       - home navigation


# Author: Debe Okoye
# Created: 2026-06-02
# ============================================================
from app.config.constants import (
	TABLE_OPERATIONS, 
	READ_VIEW_MAPPING
)
from app.ui.forms.form_mapping import FORM_MAPPING
from app.ui.dialogs import SearchDialog
from app.ui.monitor import load_monitor_table
from PyQt6.QtWidgets import (
	QFrame,
	QLabel,
	QPushButton,
	QToolBox,
	QVBoxLayout,
	QWidget
)

# ============================================================
# Sidebar Construction
# ============================================================
def build_sidebar(window) -> QWidget:
	panel = QFrame()
	panel.setObjectName("sidePanel")

	layout = QVBoxLayout(panel)
	layout.setContentsMargins(10, 10, 10, 10)
	layout.setSpacing(10)

	home_btn = QPushButton("Home")
	home_btn.setMinimumHeight(36)
	home_btn.clicked.connect(lambda: go_home(window))
	layout.addWidget(home_btn)

	toolbox =QToolBox()
	toolbox.setObjectName("toolboxHeader")

	operation_mapping ={
		"Create": "create",
		"Read": "read",
		"Update": "update",
		"Delete": "delete"
	}
	for operation,permission in operation_mapping.items():
		# Build Table Lists
		table_names = []
		for table,operations in TABLE_OPERATIONS.items():
			if operations[permission]:
				table_names.append(table)

		page = toolbox_page(window, table_names, operation)
		toolbox.addItem(page, operation)
	layout.addWidget(toolbox)

	db_panel = QFrame()
	db_panel.setObjectName("dbStatusPanel")

	panel_layout = QVBoxLayout(db_panel)
	panel_layout.setContentsMargins(8, 8, 8, 8)
	panel_title = QLabel("Database")
	panel_title.setObjectName("sectionTitle")
	
	window.db_status_label = QLabel("Status: Not Connected")
	window.db_name_label = QLabel("Database: ")
	window.db_name_label.setObjectName("mutedText")
	window.db_host_label = QLabel("Host: ")
	window.db_host_label.setObjectName("mutedText")
	window.db_user_label = QLabel("User: ")
	window.db_user_label.setObjectName("mutedText")
	window.db_last_refresh_label = QLabel("Last Refresh: ")
	window.db_last_refresh_label.setObjectName("mutedText")

	test_btn = QPushButton("Test Database Connection")
	test_btn.clicked.connect(window.test_database_connection)

	panel_layout.addWidget(panel_title)
	panel_layout.addWidget(window.db_status_label)
	panel_layout.addWidget(window.db_name_label)
	panel_layout.addWidget(window.db_host_label)
	panel_layout.addWidget(window.db_user_label)
	panel_layout.addWidget(window.db_last_refresh_label)
	panel_layout.addWidget(test_btn)

	layout.addWidget(db_panel)

	return panel

# ============================================================
# Home Navigation
# ============================================================
def go_home(window) -> None:
	window.tabs.blockSignals(True)
	window.tabs.setCurrentIndex(0)
	window.tabs.blockSignals(False)
	window.tab_stack.setCurrentIndex(0)

# ============================================================
# CRUD Toolbox Page Builder
# ============================================================
def toolbox_page(window, table_names: list[str], operation: str) -> QWidget:
	page = QWidget()
	page_layout = QVBoxLayout(page)
	page_layout.setContentsMargins(6, 6, 6, 6)
	page_layout.setSpacing(6)
	for table in table_names:
		btn = QPushButton(table)
		btn.setMinimumHeight(36)
		btn.clicked.connect(
			lambda _checked=False, op=operation, tbl=table: on_table_action(window, op, tbl)
		)
		page_layout.addWidget(btn)
	page_layout.addStretch()
	return page

# ============================================================
# CRUD Operation Router
# ============================================================
def on_table_action(window, operation: str, table: str) -> None:
	if operation == "Create":
			form_class = FORM_MAPPING[table]
			create_dialog = form_class(window, table_name=table, mode="create")
			create_dialog.exec()  

	elif operation == "Read":
		db_view = READ_VIEW_MAPPING[table]
		load_monitor_table(window, table, db_view)

		window.tabs.setCurrentIndex(1)
		window.tab_stack.setCurrentIndex(1)

	elif operation == "Update":
		search_dialog = SearchDialog(window,table)
		form_class = FORM_MAPPING[table]

		if search_dialog.exec() :
			selected_record = search_dialog.selected_record
			update_dialog = form_class(window, table_name=table, mode= "update", record_data= selected_record)
			update_dialog.exec()

	elif operation == "Delete":
		delete_dialog = SearchDialog(window, table, mode="delete")
		delete_dialog.exec()