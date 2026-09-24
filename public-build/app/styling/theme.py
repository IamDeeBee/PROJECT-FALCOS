# ============================================================
# File: theme.py
# Project: UAV Management Dashboard
# Purpose: Handles application theme styling and theme
# switching functionality.


# Description:
# Manages:
# - dark mode
# - light mode
# - application stylesheet updates
# - theme toggle behavior


# Author: Debe Okoye
# Created: 2026-06-02
# ============================================================
from PyQt6.QtWidgets import QApplication

# ============================================================
# Theme Toggle Logic
# ============================================================
def toggle_theme(window) -> None:
	window.dark_mode = window.theme_toggle.isChecked()
	window.theme_toggle.setText("Dark" if window.dark_mode else "Light")
	apply_theme(window)

# ============================================================
# Theme Application
# ============================================================
def apply_theme(window) -> None:
	if window.dark_mode:
		QApplication.instance().setStyleSheet(
			"""
			#sidePanel{ 
				background: #1A2234; 
				border: 1px solid #26324A; 
				border-radius: 8px; 
			}
			#dbStatusPanel{ 
				background: #1A2234; 
				border: 1px solid #26324A; 
				border-radius: 8px; 
			}
			#dashboardCard{ 
				background: #1A2234; 
				border: 1px solid #26324A; 
				border-radius: 8px; 
			}
			QCalendarWidget QMenu {
				background-color: white;
				color: black;
			}

			QCalendarWidget QSpinBox {
				background-color: white;
				color: black;
			}

			QCalendarWidget QToolButton {
				background-color: #1A2234;
				color: white;
				border: none;
			}
			QCheckBox {
				background: transparent;
				color: white;
				spacing: 6px;
			}
			QComboBox {
				background-color: white;
				border: 1px solid #C2D0E4;
				border-radius: 4px;
				padding: 2px 6px;
			}			
			QComboBox:on {
				color: black;
			}
			QComboBox:!on {
				color: black;
			}
			QComboBox:disabled {
				background-color: grey;
			}
			QDateEdit {
				background-color: white;
				border: 1px solid #C2D0E4;
				border-radius: 4px;
				padding: 2px 6px;
			}
			QDateEdit:!on {
				color: black;
			}
			QDateEdit:on {
				color: black;
			}
			QDateTimeEdit {
				background-color: white;
				color: black;
			}
			QDateTimeEdit:!on {
				color: black;
			}
			QDateTimeEdit:on {
				color: black;
			}
			QDialog {
				background: #2A3957;
			}
			QDoubleSpinBox {
				background-color: white;
				color: black;
			}
			QDoubleSpinBox:focus {
				color: black;
			}
			QDoubleSpinBox:!focus {
				color: black;
			}
			QDoubleSpinBox::up-button,
			QDoubleSpinBox::down-button {
				border: none;
				background: transparent;
			}
			QFrame { 
				background: #1A2234; 
				border: 1px solid #26324A; 
				border-radius: 8px; 
			}
			QLabel {
				background-color: transparent;
				border: none;
				border-radius: 0px;
				padding: 0px;
			}
			QLineEdit {
				background-color: white;
			}
			QLineEdit:focus {
				color: black;
			}
			QLineEdit:!focus {
				background-color: white;
				color: black;
			}
			QLineEdit:disabled {
				background-color: grey;
				color: black;
			}
			QLineEdit:read-only {
				background-color: grey;
			}
			QMainWindow {
				background: #101521;
			}
			QMenu {
				background-color: #1a2333;
				color: white;
				border: 1px solid #33415c;
			}

			QMenu::item {
				padding: 6px 20px;
				color: white;
			}

			QMenu::item:selected {
				background-color: #2d405f;
				color: white;
			}
			QPushButton { 
				background: #2A3957; 
				border: 1px solid #3A4E74; 
				border-radius: 6px; 
				padding: 6px 10px; 
			}
			QPushButton:hover { 
				background: #33466A; 
			}
			QTabBar::tab { 
				background: #141C2E; 
				border: 1px solid #2E3D5D; 
				border-radius: 6px; 
				padding: 6px; 
			}
			QTabBar::tab:selected { 
				background: #2E4265; 
			}
			QTextEdit {
				background-color: white;
			}
			QTextEdit:focus {
				color: black;
			}
			QTextEdit:!focus {
				background-color: white;
				color: black;
			}
			QTextEdit:read-only {
				background-color: grey;
				color: black;
			}
			QToolBox::tab { 
				background: #141C2E; 
				border: 1px solid #2E3D5D; 
				border-radius: 6px;
				font-weight: bold;  
				padding: 6px; 
			}
			QToolBox QWidget { 
				background: transparent;
			}
			QWidget { 
				color: #E6ECF3; 
				font-size: 13px; 
			}
			#sectionTitle { 
				font-size: 18px; 
				font-weight: 600;
			}
			#summaryValue {
				font-size: 14pt;
				font-weight: bold;
				color: #7BC8F6;
			}
			#valueText { 
			 	font-size: 22px; 
				font-weight: 700; 
				color: #7BC8F6; 
			}
			#mutedText { 
				color: #A8B7CF; 
			}
		"""
		)
	else:
		QApplication.instance().setStyleSheet(
			"""
			#sidePanel{ 
				background: #FFFFFF; 
				border: 1px solid #D7DEE9; 
				border-radius: 8px; 
			}
			#dbStatusPanel{ 
				background: #FFFFFF; 
				border: 1px solid #D7DEE9; 
				border-radius: 8px; 
			}
			#dashboardCard{ 
				background: #FFFFFF; 
				border: 1px solid #D7DEE9; 
				border-radius: 8px; 
			}		
			QComboBox {
				background-color: white;
				color: black;
			}
			QComboBox:disabled {
				background-color: grey;
			}
			QDateEdit {
				background-color: white;
				color: black;
			}
			QDateTimeEdit {
				background-color: white;
				color: black;
			}
			QDialog {
				background: #EEF2F8; 
			}
			QDoubleSpinBox {
				background-color: white;
				color: black;
			}
			QFrame { 
				background: #FFFFFF; 
				border: 1px solid #D7DEE9; 
				border-radius: 8px; 
			}
			QLabel {
				background-color: transparent;
				border: none;
				border-radius: 0px;
				padding: 0px;
			}
			QLineEdit {
				background-color: white;
				color: black;
			}
			QLineEdit:disabled {
				background-color: grey;
				color: black;
			}
			QLineEdit:read-only {
				background-color: grey;
			}
			QMainWindow {
				background: #EEF2F8; 
			}
			QPushButton { 
				background: #E8EEF8; 
				border: 1px solid #C2D0E4; 
				border-radius: 6px; 
				padding: 6px 10px; 
			}
			QPushButton:hover { 
				background: #DCE6F6; 
			}
			QTabBar::tab { 
				background: #FFFFFF; 
				border: 1px solid #CCD6E4; 
				border-radius: 6px; 
				padding: 6px; 
			}
			QTabBar::tab:selected { 
				background: #DCE8F8; 
			}
			QTextEdit {
				background-color: white;
				color: black;
			}
			QTextEdit:read-only {
				background-color: grey;
				color: black;
			}
			QToolBox::tab { 
				background: #FFFFFF; 
				border: 1px solid #CCD6E4; 
				border-radius: 6px;
				font-weight: bold; 
				padding: 6px; 
			}
			QToolBox QWidget { 
				background: transparent; 
			}
			QWidget { 
				color: #1F2A3A; 
				font-size: 13px; 
			}
			#sectionTitle { 
				font-size: 18px; 
				font-weight: 600;
			}
			#summaryValue {
				font-size: 14pt;
				font-weight: bold;
				color: #2563EB;
			}
			#valueText { 
				font-size: 22px; 
				font-weight: 700; 
				color: #2563EB; 
			}
			#mutedText { 
				color: #5B6578; 
			}
		"""
		)