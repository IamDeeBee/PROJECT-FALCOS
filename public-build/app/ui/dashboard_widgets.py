# ============================================================
# File:         dashboard_widgets.py
# Project:      UAV Management Dashboard
# Purpose:      Stores dashboard widget creation functions.
#
# Description:
#   Contains reusable dashboard UI components such as:
#   - summary cards
#   - calendar widget
#   - PostgreSQL status card
#   - activity panels
#
# Author: Debe Okoye
# Created: 2026-06-02
# ============================================================

from app.database.dashboard_repository import *
from app.database.connection import get_connection
from PyQt6.QtGui import QFont
from PyQt6.QtCore import (
	QDateTime,
	Qt,
	QTimer
)
from PyQt6.QtWidgets import (
	QFrame,
	QGridLayout,
	QLabel,
	QListWidget,
	QMessageBox,
	QVBoxLayout,
	QWidget    
)

# ============================================================
# Dashboard Page Construction
# ============================================================
def build_dashboard_page(window) -> QWidget:

	# Builds the main dashboard layout
	page = QWidget()
	grid = QGridLayout(page)
	grid.setContentsMargins(0, 0, 0, 0)
	grid.setHorizontalSpacing(10)
	grid.setVerticalSpacing(10)

	calendar_card = make_datetime_card(window)
	personnel_card = make_personnel_card(window)
	pilot_certification_card = make_certification_card(window)

	flight_card = make_flight_card(window)
	uav_card = make_fleet_card(window)
	maintenance_card = make_maintenance_card(window)
	   
	alert_card = make_alert_card(window)
	activity_card = make_activity_card(window)

	grid.addWidget(calendar_card,               0, 0, 1, 1)
	grid.addWidget(personnel_card,           	0, 1, 1, 1)
	grid.addWidget(pilot_certification_card, 	0, 2, 1, 1)

	grid.addWidget(maintenance_card,			1, 0, 1, 1)
	grid.addWidget(flight_card,					1, 1, 1, 1)
	grid.addWidget(uav_card,					1, 2, 1, 1)

	grid.addWidget(alert_card,					2, 0, 1, 1)
	grid.addWidget(activity_card,				2, 1, 1, 2)

	grid.setColumnStretch(0, 1)
	grid.setColumnStretch(1, 1)
	grid.setColumnStretch(2, 1)
	
	grid.setRowStretch(0, 1)
	grid.setRowStretch(1, 1)
	grid.setRowStretch(2, 1)


	return page

# ============================================================
# Refresh Dashboard Card
# ============================================================
def refresh_dashboard(window):

	conn = None

	try:
		conn = get_connection()

		window.alert_summary = get_alert_summary(conn)
		window.certification_summary = get_certification_summary(conn)
		window.fleet_summary = get_fleet_summary(conn)
		window.flight_summary = get_flight_summary(conn)
		window.maintenance_summary = get_maintenance_summary(conn)
		window.personnel_summary = get_personnel_summary(conn)

		update_alert_card(window)
		update_certification_card(window)
		update_fleet_card(window)
		update_flight_card(window)
		update_maintenance_card(window)
		update_personnel_card(window)

	except Exception as e:
		QMessageBox.critical(
			window,
			"Dashboard Refresh Error",
			f"Failed to refresh the dashboard.\n\n{e}"
		)
	finally:
		if conn:
			conn.close()

# ============================================================
# Generic Dashboard Card
# ============================================================
def make_card(title: str, value: str) -> QFrame:

	# Creates reusable dashboard summary card.
	card = QFrame()
	card.setObjectName("dashboardCard")
	layout = QVBoxLayout(card)
	t = QLabel(title)
	t.setObjectName("sectionTitle")
	v = QLabel(value)
	v.setObjectName("valueText")
	layout.addWidget(t)
	layout.addStretch()
	layout.addWidget(v)
	return card

# ============================================================
# Calendar / Date-Time Card
# ============================================================
def make_datetime_card(window) -> QFrame:
	# Creates live date and time dashboard card.
	card = QFrame()
	card.setObjectName("dashboardCard")
	layout = QVBoxLayout(card)
	title = QLabel("Calendar")
	title.setObjectName("sectionTitle")
	window.datetime_label = QLabel()
	window.datetime_label.setObjectName("valueText")
	window.datetime_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
	layout.addWidget(title)
	layout.addStretch()
	layout.addWidget(window.datetime_label)

	update_datetime_label(window)
	timer = QTimer(window)
	timer.timeout.connect(lambda: update_datetime_label(window))
	timer.start(1000)
	return card
def update_datetime_label(window) -> None:
	# Updates live date and time display.
	now = QDateTime.currentDateTime()
	window.datetime_label.setText(
		f"{now.toString('dddd, MMMM d, yyyy')}\n{now.toString('h:mm:ss AP')}"
	)

# ============================================================
# Personnel Card
# ============================================================
def make_personnel_card(window) -> QFrame:
	
	card = QFrame()
	card.setObjectName("dashboardCard")
	
	layout = QVBoxLayout(card)
	
	personnel_title = QLabel("Personnel")
	personnel_title.setObjectName("sectionTitle")

	total_personnel_label = QLabel("Total Personnel")
	window.total_personnel_value = QLabel("--")
	window.total_personnel_value.setObjectName("summaryValue")

	active_pilot_label = QLabel("Active Pilots")
	window.active_pilot_value = QLabel("--")
	window.active_pilot_value.setObjectName("summaryValue")

	technicians_label = QLabel("Technicians")
	window.technicians_value = QLabel("--")
	window.technicians_value.setObjectName("summaryValue")

	layout.addWidget(personnel_title)
	layout.addSpacing(30)

	layout.addWidget(total_personnel_label)
	layout.addWidget(window.total_personnel_value)

	layout.addSpacing(20)

	layout.addWidget(active_pilot_label)
	layout.addWidget(window.active_pilot_value)
	layout.addSpacing(8)

	layout.addWidget(technicians_label)
	layout.addWidget(window.technicians_value)
	layout.addSpacing(8)
	
	return card
def update_personnel_card(window) -> None:

	summary = window.personnel_summary

	window.total_personnel_value.setText(
		str(summary["total_personnel"])
	)
	window.active_pilot_value.setText(
		str(summary["active_pilots"])
	)
	window.technicians_value.setText(
		str(summary["total_technicians"])
	)

# ============================================================
# Certification Card
# ============================================================
def make_certification_card(window)-> QFrame:
	card = QFrame()
	card.setObjectName("dashboardCard")
	
	layout = QVBoxLayout(card)
	
	certification_title = QLabel("Certifications")
	certification_title.setObjectName("sectionTitle")

	total_certification_label = QLabel("Certifications Offered")
	window.total_certification_value = QLabel("--")
	window.total_certification_value.setObjectName("summaryValue")

	active_pilot_certification_label = QLabel("Active Pilot Certifications")
	window.active_pilot_certification_value = QLabel("--")
	window.active_pilot_certification_value.setObjectName("summaryValue")

	layout.addWidget(certification_title)

	layout.addSpacing(30)

	layout.addWidget(total_certification_label)
	layout.addWidget(window.total_certification_value)

	layout.addSpacing(20)

	layout.addWidget(active_pilot_certification_label)
	layout.addWidget(window.active_pilot_certification_value)

	layout.addStretch()
	
	return card
def update_certification_card(window) -> None:
	summary = window.certification_summary

	window.total_certification_value.setText(
		str(summary["total_certifications"])
	)
	window.active_pilot_certification_value.setText(
		str(summary["active_pilot_certification"])
	)

# ============================================================
# Flight Operations Card
# ============================================================
def make_flight_card(window)-> QFrame:
	card = QFrame()
	card.setObjectName("dashboardCard")
	
	layout = QVBoxLayout(card)
	
	flight_operations_title = QLabel("Flight Operations")
	flight_operations_title.setObjectName("sectionTitle")

	total_flight_label = QLabel("All Flight Operations")
	window.total_flight_value = QLabel("--")
	window.total_flight_value.setObjectName("summaryValue")

	scheduled_label = QLabel("Scheduled")
	window.scheduled_value = QLabel("--")
	window.scheduled_value.setObjectName("summaryValue")

	progress_label = QLabel("In Progress")
	window.progress_value = QLabel("--")
	window.progress_value.setObjectName("summaryValue")
	
	layout.addWidget(flight_operations_title)

	layout.addSpacing(30)

	layout.addWidget(total_flight_label)
	layout.addWidget(window.total_flight_value)
	
	layout.addSpacing(20)

	layout.addWidget(scheduled_label)
	layout.addWidget(window.scheduled_value)
	layout.addSpacing(8)
	
	layout.addWidget(progress_label)
	layout.addWidget(window.progress_value)
	layout.addSpacing(8)
	
	layout.addStretch()
	
	return card
def update_flight_card(window) -> None:
	summary = window.flight_summary

	window.total_flight_value.setText(
		str(summary["total_flight"])
	)
	window.scheduled_value.setText(
		str(summary["scheduled"])
	)
	window.progress_value.setText(
		str(summary["progress"])
	)

# ============================================================
# UAV Card
# ============================================================
def make_fleet_card(window)-> QFrame:
	card = QFrame()
	card.setObjectName("dashboardCard")
	
	layout = QVBoxLayout(card)
	
	fleet_title = QLabel("UAV Fleet")
	fleet_title.setObjectName("sectionTitle")

	total_fleet_label = QLabel("Total Fleet Asset")
	window.total_fleet_value = QLabel("--")
	window.total_fleet_value.setObjectName("summaryValue")

	operational_label = QLabel("Operational")
	window.operational_value = QLabel("--")
	window.operational_value.setObjectName("summaryValue")

	reserved_label = QLabel("Reserved")
	window.reserved_value = QLabel("--")
	window.reserved_value.setObjectName("summaryValue")

	in_flight_label = QLabel("In Flight")
	window.in_flight_value = QLabel("--")
	window.in_flight_value.setObjectName("summaryValue")

	grounded_label = QLabel("Grounded")
	window.grounded_value = QLabel("--")
	window.grounded_value.setObjectName("summaryValue")

	decommissioned_label = QLabel("Decommissioned")
	window.decommissioned_value = QLabel("--")
	window.decommissioned_value.setObjectName("summaryValue")

	maintenance_label = QLabel("Maintenance")
	window.maintenance_value = QLabel("--")
	window.maintenance_value.setObjectName("summaryValue")	

	layout.addWidget(fleet_title)
	layout.addSpacing(30)

	layout.addWidget(total_fleet_label)
	layout.addWidget(window.total_fleet_value)
	layout.addSpacing(30)

	grid = QGridLayout()
	grid.setHorizontalSpacing(20)
	grid.setVerticalSpacing(8)
	
	grid.addWidget(operational_label,      		0, 0)
	grid.addWidget(window.operational_value, 	1, 0)
	
	grid.addWidget(reserved_label,         		2, 0)
	grid.addWidget(window.reserved_value,  		3, 0)

	grid.addWidget(in_flight_label,        		4, 0)
	grid.addWidget(window.in_flight_value, 		5, 0)

	grid.addWidget(grounded_label,         		0, 1)
	grid.addWidget(window.grounded_value, 		1, 1)

	grid.addWidget(maintenance_label,      		2, 1)
	grid.addWidget(window.maintenance_value, 	3, 1)

	grid.addWidget(decommissioned_label,      	4, 1)
	grid.addWidget(window.decommissioned_value, 5, 1)

	layout.addLayout(grid)
	layout.addStretch()
	
	return card
def update_fleet_card(window) -> None:
	summary = window.fleet_summary

	window.total_fleet_value.setText(
		str(summary["total_fleet"])
	)
	window.operational_value.setText(
		str(summary["operational"])
	)
	window.reserved_value.setText(
		str(summary["reserved"])
	)
	window.in_flight_value.setText(
		str(summary["in_flight"])
	)
	window.grounded_value.setText(
		str(summary["grounded"])
	)
	window.decommissioned_value.setText(
		str(summary["decommissioned"])
	)
	window.maintenance_value.setText(
		str(summary["maintenance"])
	)

# ============================================================
# Maintenance Card
# ============================================================
def make_maintenance_card(window)-> QFrame:
	card = QFrame()
	card.setObjectName("dashboardCard")
	
	layout = QVBoxLayout(card)
	
	maintenance_title = QLabel("Maintenance")
	maintenance_title.setObjectName("sectionTitle")

	total_maintenance_label = QLabel("Total Maintenance Order")
	window.total_maintenance_value = QLabel("--")
	window.total_maintenance_value.setObjectName("summaryValue")

	reported_label = QLabel("Reported")
	window.reported_value = QLabel("--")
	window.reported_value.setObjectName("summaryValue")

	progress_label = QLabel("In Progress")
	window.progress_value = QLabel("--")
	window.progress_value.setObjectName("summaryValue")

	layout.addWidget(maintenance_title)

	layout.addSpacing(30)

	layout.addWidget(total_maintenance_label)
	layout.addWidget(window.total_maintenance_value)

	layout.addSpacing(20)

	layout.addWidget(reported_label)
	layout.addWidget(window.reported_value)
	layout.addSpacing(8)

	layout.addWidget(progress_label)
	layout.addWidget(window.progress_value)
	layout.addSpacing(8)

	layout.addStretch()
	
	return card
def update_maintenance_card(window) -> None:
	summary = window.maintenance_summary

	window.total_maintenance_value.setText(
		str(summary["total_maintenance"])
	)
	window.reported_value.setText(
		str(summary["reported"])
	)
	window.progress_value.setText(
		str(summary["progress"])
	)

# ============================================================
# Alerts Card
# ============================================================
def make_alert_card(window)-> QFrame:
	card = QFrame()
	card.setObjectName("dashboardCard")
	
	layout = QVBoxLayout(card)
	
	alerts_title = QLabel("Alerts")
	alerts_title.setObjectName("sectionTitle")

	total_alerts_label = QLabel("Total Alerts")
	window.total_alerts_value = QLabel("--")
	window.total_alerts_value.setObjectName("summaryValue")

	pilot_pending_verification_label = QLabel("Unverified Pilots")
	window.pilot_pending_verification_value = QLabel("--")
	window.pilot_pending_verification_value.setObjectName("summaryValue")

	certification_pending_label = QLabel("Pending Pilot Certifications")
	window.certification_pending_value = QLabel("--")
	window.certification_pending_value.setObjectName("summaryValue")

	certification_expired_label = QLabel("Expired Certification")
	window.certification_expired_value = QLabel("--")
	window.certification_expired_value.setObjectName("summaryValue")

	certification_to_expired_label = QLabel("Certifications About to Expire")
	window.certification_to_expired_value = QLabel("--")
	window.certification_to_expired_value.setObjectName("summaryValue")
	
	reservation_pending_validation_label = QLabel("Unvalidated Reservations")
	window.reservation_pending_validation_value = QLabel("--")
	window.reservation_pending_validation_value.setObjectName("summaryValue")

	maintenance_reported_label = QLabel("Maintenance Reported")
	window.maintenance_reported_value = QLabel("--")
	window.maintenance_reported_value.setObjectName("summaryValue")
	
	layout.addWidget(alerts_title)
	layout.addSpacing(30)

	layout.addWidget(total_alerts_label)
	layout.addWidget(window.total_alerts_value)
	layout.addSpacing(20)

	grid = QGridLayout()
	grid.setHorizontalSpacing(20)
	grid.setVerticalSpacing(8)
	

	grid.addWidget(pilot_pending_verification_label, 			0, 0)
	grid.addWidget(window.pilot_pending_verification_value,		1, 0)

	grid.addWidget(certification_pending_label, 				0, 1)
	grid.addWidget(window.certification_pending_value,			1, 1)
	
	grid.addWidget(certification_to_expired_label,				2, 0)
	grid.addWidget(window.certification_to_expired_value,		3, 0)
	
	grid.addWidget(certification_expired_label,					2, 1)
	grid.addWidget(window.certification_expired_value,			3, 1)
	
	grid.addWidget(reservation_pending_validation_label,		4, 0)
	grid.addWidget(window.reservation_pending_validation_value,	5, 0)
	
	grid.addWidget(maintenance_reported_label,					4, 1)
	grid.addWidget(window.maintenance_reported_value,			5, 1)
	
	layout.addLayout(grid)
	layout.addStretch()
	
	return card
def update_alert_card(window) -> None:
	summary = window.alert_summary

	total_alerts = sum(summary.values())

	window.total_alerts_value.setText(
		str(total_alerts)
	)
	window.pilot_pending_verification_value.setText(
		str(summary["pilot_pending_verification"])
	)
	window.certification_pending_value.setText(
		str(summary["certification_pending"])
	)
	window.certification_to_expired_value.setText(
		str(summary["certification_to_expired"])
	)
	window.certification_expired_value.setText(
		str(summary["certification_expired"])
	)
	window.reservation_pending_validation_value.setText(
		str(summary["reservation_pending_validation"])
	)
	window.maintenance_reported_value.setText(
		str(summary["maintenance_reported"])
	)

# ============================================================
# Activity Card
# ============================================================
def make_activity_card(window) -> QFrame:
		
	# Creates recent activity dashboard card.
	
	card = QFrame()
	card.setObjectName("dashboardCard")
	layout = QVBoxLayout(card)

	title = QLabel("Activity Performed")
	title.setObjectName("sectionTitle")

	window.activity_feed = QListWidget()
	window.activity_feed.setObjectName("mutedList")
	window.activity_feed.setWordWrap(True)

	layout.addWidget(title)
	layout.addWidget(window.activity_feed)
	
	return card