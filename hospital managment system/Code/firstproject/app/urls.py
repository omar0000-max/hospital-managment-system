from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path("", views.home_view, name="home"),
    path("patients/", views.patients_view, name="patients"),
    path("medicines/", views.medicines_view, name="medicines"),
    path("prescription/", views.prescription_view, name="prescription"),
    path("appointments/", views.appointments_view, name="appointments"),
    path("doctors/", views.doctors_view, name="doctors"),
    path("doctors/<int:id>/", views.doctor_detail, name="doctor_detail"),

    # Page Actions
    path("patients/delete/<int:id>/", views.delete_patient, name="delete_patient"),
    path("medicines/delete/<int:id>/", views.delete_medicine, name="delete_medicine"),
    path("appointments/cancel/<int:id>/", views.cancel_appointment, name="cancel_appointment"),

    # API — Fetch
    path("api/patients/", views.api_patients),
    path("api/doctors/", views.api_doctors),
    path("api/medicines/", views.api_medicines),

    # API — Create
    path("api/patients/add/", views.api_add_patient),
    path("api/medicines/add/", views.api_add_medicine),
    path("api/doctors/add/", views.api_add_doctor),
    path("api/prescription/create/", views.api_create_prescription),
    path("api/appointment/create/", views.api_create_appointment),

    # API — Delete
    path("api/medicine/delete/<int:id>/", views.delete_medicine),
]

    