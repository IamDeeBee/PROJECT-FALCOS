# ============================================================
# File:        constants.py
# Project:     UAV Management Dashboard
# Purpose:     Stores reusable constant values used across
#              the application.
#
# Description:
#     Contains static configuration values such as:
#     - table names
#     - statuses
#     - labels
#     - future configuration constants
#
# Author:      Debe Okoye
# Created:     2026-06-02
# ============================================================

# ============================================================
# Database Table Names
# ============================================================

DB_SCHEMA = "uav_system"

DEMO_MODE = True

FLIGHT_LOCATIONS = ("FRIA","INDOOR","SPECIFIC")

FORM_VALID_MODES =("create","update")

MAINTENANCE_TYPE = ( "PREVENTIVE","CORRECTIVE","PREDICTIVE","CONDITION_BASED")

TABLE_MAPPING = {
	"Certification" : "certifications", 
	"Company" : "company",
	"Flight Logs" : "flight_logs",
	"Maintenance Logs" : "maintenance_logs",
	"Maintenance Order" : "maintenance_logs",
	"Personnel" : "person",
	"Pilots" : "pilot", 
	"Pilot Certifications" : "pilot_certification",
	"Reservations" : "flight_reservations", 
	"Technicians" : "technician",
	"UAV": "fleet_asset"
}

TABLE_OPERATIONS = {
	"Certification"         :   {"create": True , "read": True, "update": True, "delete": True}, 
	"Company"               :   {"create": True , "read": True, "update": True, "delete": True},
	"Flight Logs"           :   {"create": True, "read": True, "update": True, "delete": True},
	"Maintenance Logs"      :   {"create": True, "read": True, "update": True, "delete": True},
	"Maintenance Order"     :   {"create": True , "read": True, "update": True, "delete": True},
	"Personnel"             :   {"create": True , "read": True, "update": True, "delete": True},
	"Pilots"                :   {"create": True, "read": True, "update": True, "delete": True}, 
	"Pilot Certifications"  :   {"create": True , "read": True, "update": True, "delete": True},
	"Reservations"          :   {"create": True , "read": True, "update": True, "delete": True}, 
	"Technicians"           :   {"create": True, "read": True, "update": True, "delete": True},
	"UAV"                   :   {"create": True , "read": True, "update": True, "delete": True}
}


READ_VIEW_MAPPING = {
	"Certification": "vw_all_certifications",
	"Company" : "vw_all_companies",
	"Flight Logs": "vw_all_flight_logs",
	"Maintenance Logs": "vw_all_maintenance_logs",
	"Maintenance Order": "vw_all_maintenance_orders",
	"Personnel": "vw_all_personnel",
	"Pilots" : "vw_all_pilots",
	"Pilot Certifications" : "vw_all_pilot_certifications",
	"Reservations": "vw_all_flight_reservations",
	"Technicians": "vw_all_technicians",
	"UAV": "vw_all_fleet_assets"   
}

SEARCH_DIALOG_MAPPING = {
	"Certification"			: {"view": "vw_all_certifications",			"table": "certifications",         "search_column": "name",				"primary_key": "cert_id",					"search_label": "Certification Name"},
	"Company" 				: {"view": "vw_all_companies",				"table": "company",                "search_column": "name",				"primary_key": "company_id",				"search_label": "Company Name"},
	"Flight Logs"			: {"view": "vw_all_flight_logs",			"table": "flight_logs",            "search_column": "id",				"primary_key": "log_id",					"search_label": "Flight Log ID"},
	"Maintenance Logs"		: {"view": "vw_all_maintenance_logs",		"table": "maintenance_logs",       "search_column": "id",				"primary_key": "maint_id",					"search_label": "Maintenance Log ID"},
	"Maintenance Order"		: {"view": "vw_all_maintenance_orders",		"table": "maintenance_logs",       "search_column": "id",				"primary_key": "maint_id", 					"search_label": "Maintenance OrderID"},
	"Personnel"				: {"view": "vw_all_personnel",				"table": "person",                 "search_column": "full_name",		"primary_key": "person_id",					"search_label": "Full Name"},
	"Pilots"				: {"view": "vw_all_pilots",					"table": "pilot",                  "search_column": "full_name",		"primary_key": "pilot_id",					"search_label": "Full Name"},
	"Pilot Certifications"	: {"view": "vw_all_pilot_certifications",	"table": "pilot_certification",    "search_column": "full_name",		"primary_key": "pilcert_id",				"search_label": "Full Name"},
	"Reservations"			: {"view": "vw_all_flight_reservations",	"table": "flight_reservations",    "search_column": "id",				"primary_key": "reserv_id",					"search_label": "Flight Reservation ID"},
	"Technicians"			: {"view": "vw_all_technicians",			"table": "technician",             "search_column": "full_name",		"primary_key": "technician_id",				"search_label": "Full Name"},
	"UAV"					: {"view": "vw_all_fleet_assets",			"table": "fleet_asset",            "search_column": "nickname",			"primary_key": "asset_id",					"search_label": "UAV Nickname"}

}