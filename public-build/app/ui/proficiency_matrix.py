# ============================================================
# File:         proficiency_matrix.py
# Project:      UAV Management Dashboard
# Purpose:      Proficiency matrix construction and management
#               functionality.
#
# Description:
#       Handles:
#       - proficiency matrix layout
#       - refresh system
#       - dynamic table viewing 
#		- dynamic table updating
#       - proficiency table population
#
# Author: Debe Okoye
# Created: 2026-08-19
# ============================================================
from app.database.proficiency_repository import (
	get_proficiency_data,
	update_proficiency_levels
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
	QColor,
	QPainter
)
from PyQt6.QtWidgets import (
	QHBoxLayout,
	QHeaderView,
	QLabel,
	QMessageBox,
	QPushButton,
	QStyleOptionHeader, QStyle, 
	QTableWidget,
	QTableWidgetItem,
	QVBoxLayout,
	QWidget
)

# ============================================================
# Wrapped Table Header
# ============================================================
class WrappedHeader(QHeaderView):

	def paintSection(self, painter, rect, logicalIndex):
		if not rect.isValid():
			return

		model = self.model()
		text = model.headerData(
			logicalIndex,
			self.orientation(),
			Qt.ItemDataRole.DisplayRole
		)

		option = QStyleOptionHeader()
		self.initStyleOption(option)
		option.rect = rect
		option.text = ""

		self.style().drawControl(
			QStyle.ControlElement.CE_Header,
			option,
			painter,
			self
		)

		painter.save()

		painter.drawText(
			rect.adjusted(5, 2, -5, -2),
			Qt.AlignmentFlag.AlignCenter |
			Qt.TextFlag.TextWordWrap,
			str(text)
		)

		painter.restore()

# ============================================================
# Proficiency Matrix Page Construction
# ============================================================
def build_proficiency_page(window) -> QWidget:
	page = QWidget()

	layout = QVBoxLayout(page)

	top_bar = QHBoxLayout()

	window.proficiency_label = QLabel("Pilot-UAV Proficiency Matrix")

	update_btn = QPushButton("Update")
	update_btn.clicked.connect(lambda: update_proficiency_table(window))

	refresh_btn = QPushButton("Refresh")
	refresh_btn.clicked.connect(lambda: refresh_proficiency_table(window))

	top_bar.addWidget(window.proficiency_label)
	top_bar.addStretch()
	top_bar.addWidget(update_btn)
	top_bar.addWidget(refresh_btn)
	
	window.proficiency_table = QTableWidget()
	window.proficiency_table.horizontalHeader().setTextElideMode(Qt.TextElideMode.ElideNone)
	window.proficiency_table.setHorizontalHeader(WrappedHeader(Qt.Orientation.Horizontal))
	window.proficiency_table.horizontalHeader().setMinimumHeight(60)
	

	window.proficiency_changes = {}
	window.proficiency_table.itemChanged.connect(
		lambda item: track_proficiency_change(window, item)
	)

	layout.addLayout(top_bar)
	layout.addWidget(window.proficiency_table)

	return page

# ============================================================
# Refresh Proficiency Table
# ============================================================
def refresh_proficiency_table(window) -> None:
	try:
		proficiency_raw = get_proficiency_data()

		# Extract Unique Pilot Names and UAV Nicknames
		pilots = sorted({
			row['full_name']
			for row in proficiency_raw
		})
		uavs = sorted({
			row['uav_nickname']
			for row in proficiency_raw
		})

		window.proficiency_table.blockSignals(True)

		window.proficiency_table.setRowCount(len(pilots))
		window.proficiency_table.setColumnCount(len(uavs))

		window.proficiency_table.setHorizontalHeaderLabels(uavs)

		pilot_rows = {
			pilot:index
			for index,pilot in enumerate(pilots)
		}

		uav_columns = {
			uav:index
			for index,uav in enumerate(uavs)
		}

		for row in proficiency_raw:
			pilot = row["full_name"]
			uav = row["uav_nickname"]
			level = row["proficiency_level"]

			row_index = pilot_rows[pilot]
			column_index = uav_columns[uav]

			item = QTableWidgetItem(str(level))
			item.setData(Qt.ItemDataRole.UserRole, row['id'])
			item.setData(Qt.ItemDataRole.UserRole+1, level)
			item.setBackground(get_proficiency_color(level))
			window.proficiency_table.setItem(
				row_index,
				column_index,
				item
			)

		window.proficiency_table.setVerticalHeaderLabels(pilots)
		

	except Exception as e:
		QMessageBox.critical(
			window, 
			"Database Error", 
			f"Failed to connect to the database: \n\n{e}"
		)

	finally:
		window.proficiency_table.blockSignals(False)



# ============================================================
# Proficiency Level Color
# ============================================================
def get_proficiency_color(level):
	if level == 0:
		return QColor("#444444")
	elif level == 1:
		return QColor("#C9A227")
	elif level == 2:
		return QColor("#4CAF50")
	elif level == 3:
		return QColor("#2196F3")
	else:
		return QColor("#444444")

# ============================================================
# Track Proficiency Changes
# ============================================================
def track_proficiency_change(window, item) -> None:
	record_id = item.data(Qt.ItemDataRole.UserRole)
	original_level = item.data(Qt.ItemDataRole.UserRole + 1)

	try:
		current_level = int(item.text())
	except ValueError:
		current_level = None

	if current_level == original_level:
		window.proficiency_changes.pop(record_id, None)
	else:
		window.proficiency_changes[record_id] =  {
			"item": item,
			"level": current_level
		}

# ============================================================
# Validate Proficiency Changes
# ============================================================
def validate_proficiency_changes(window) -> bool:
	valid = True

	for change in window.proficiency_changes.values():

		item = change["item"]
		try:
			level = int(item.text())
		except ValueError:
			level = None

		if level not in (0, 1, 2, 3):
			item.setBackground(QColor("#FF051E"))
			valid = False
		else:
			item.setBackground(get_proficiency_color(level))

	return valid

# ============================================================
# Update Proficiency Change 
# ============================================================
def update_proficiency_table(window) -> None:
	if not window.proficiency_changes:
		QMessageBox.information(
			window,
			"Update",
			"No proficiency changes to save."
		)
		return

	if not validate_proficiency_changes(window):
		QMessageBox.warning(
			window,
			"Validation Error",
			"Please correct the highlighted proficiency values."
		)
		return

	try:		
		update_proficiency_levels(window.proficiency_changes)

		window.proficiency_changes.clear()

		refresh_proficiency_table(window)

		QMessageBox.information(
			window,
			"Success",
			"Proficiency matrix updated successfully."
		)

	except Exception as e:
		QMessageBox.critical(
			window,
			"Update Error",
			f"Failed to update the proficiency matrix:\n\n{e}"
		)
