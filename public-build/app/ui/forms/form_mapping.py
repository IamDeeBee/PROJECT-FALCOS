from app.ui.forms import (
    CertificationForm,
    CompanyForm,
    FlightLogForm,
    MaintenanceLogForm,
    MaintenanceOrderForm,
    PersonForm,
    PilotForm,
    PilotCertificationForm,
    ReservationForm,
    TechnicianForm,
    UAVForm
)

FORM_MAPPING = {
    "Certification"            : CertificationForm,
    "Company"                  : CompanyForm,
    "Flight Logs"              : FlightLogForm,
    "Maintenance Logs"         : MaintenanceLogForm,
    "Maintenance Order"        : MaintenanceOrderForm,
    "Personnel"                : PersonForm,
    "Pilots"                   : PilotForm,
    "Pilot Certifications"     : PilotCertificationForm,
    "Reservations"             : ReservationForm,
    "Technicians"              : TechnicianForm,
    "UAV"                      : UAVForm
}