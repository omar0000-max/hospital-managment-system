from django.shortcuts import render, redirect
from .models import Patient
from .models import Prescription, Appointment, Medicine, PrescriptionItem
from django.core.exceptions import ValidationError
from .models import Appointment, Doctor
from django.http import JsonResponse
from .models import Medicine
import json
from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    return render(request, "app/home.html")

def patients_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        Patient.objects.create(name=name, phone=phone)
        return redirect("patients")

    #patients = Patient.objects.all()
    patients = Patient.objects.filter(is_active=True)
    return render(request, "app/patients.html", {"patients": patients})

def medicines_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")

        Medicine.objects.create(
            name=name,
            quantity=quantity,
            price=price
        )
        return redirect("medicines")

    medicines = Medicine.objects.all()
    return render(request, "app/medicine.html", {"medicines": medicines})

def prescription_view(request):
    appointments = Appointment.objects.all()
    medicines = Medicine.objects.all()
    items = PrescriptionItem.objects.all()   

    if request.method == "POST":
        appointment_id = request.POST.get("appointment")
        medicine_id = request.POST.get("medicine")
        quantity = int(request.POST.get("quantity"))

        try:
            appointment = Appointment.objects.get(id=appointment_id)
            medicine = Medicine.objects.get(id=medicine_id)

            prescription, created = Prescription.objects.get_or_create(
                appointment=appointment
            )

            PrescriptionItem.objects.create(
                prescription=prescription,
                medicine=medicine,
                quantity=quantity
            )

        except ValidationError as e:
            return render(request, "app/prescription.html", {
                "appointments": appointments,
                "medicines": medicines,
                "items": items,   
                "error": str(e)
            })

        return redirect("prescription")

    return render(request, "app/prescription.html", {
        "appointments": appointments,
        "medicines": medicines,
        "items": items   
    })

def appointments_view(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")

        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            status="Pending"
        )
    if request.method == "POST" and "status_update" in request.POST:
        appointment_id = request.POST.get("appointment_id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = "Completed"
        appointment.save()
        return redirect("appointments")

    appointments = Appointment.objects.all()

    return render(request, "app/appointments.html", {
        "patients": patients,
        "doctors": doctors,
        "appointments": appointments
    })

def delete_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.is_active = False   
    patient.save()
    return redirect("patients")

def delete_medicine(request, id):
    med = Medicine.objects.get(id=id)
    med.delete()
    return redirect("medicines")

def cancel_appointment(request, id):
    if request.method == "POST":
        appointment = Appointment.objects.get(id=id)
        appointment.status = "Cancelled"
        appointment.save()
    return redirect("appointments")
def doctors_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        specialization = request.POST.get("specialization")

        Doctor.objects.create(
            name=name,
            specialization=specialization
        )
        return redirect("doctors")

    doctors = Doctor.objects.all()
    return render(request, "app/doctors.html", {"doctors": doctors})

def doctor_detail(request, id):
    doctor = Doctor.objects.get(id=id)
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, "app/doctor_detail.html", {
        "doctor": doctor,
        "appointments": appointments
    })

def api_patients(request):
    data = list(Patient.objects.values())
    return JsonResponse(data, safe=False)

def api_doctors(request):
    data = list(Doctor.objects.values())
    return JsonResponse(data, safe=False)    

def api_medicines(request):
    data = list(Medicine.objects.values())
    return JsonResponse(data, safe=False)


#from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def api_add_medicine(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Medicine.objects.create(
            name=data["name"],
            quantity=data["quantity"],
            price=data["price"]
        )

        return JsonResponse({"message": "Added successfully"})
# Create your views here.
#from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def api_add_patient(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Patient.objects.create(
            name=data["name"],
            phone=data["phone"]
        )
        return JsonResponse({"message": "Patient added"})
#from django.views.decorators.csrf import csrf_exempt    
@csrf_exempt
def delete_medicine(request, id):
    med = Medicine.objects.get(id=id)
    med.delete()
    return JsonResponse({"message": "Deleted"})
    
#from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def api_add_doctor(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Doctor.objects.create(
            name=data["name"],
            specialization=data["specialization"]
        )

        return JsonResponse({"message": "Doctor added successfully"})
    
@csrf_exempt
def api_add_prescription_item(request):
    if request.method == "POST":
        data = json.loads(request.body)

        prescription_id = data["prescription_id"]
        medicine_id = data["medicine_id"]
        quantity = data["quantity"]

        prescription = Prescription.objects.get(id=prescription_id)
        medicine = Medicine.objects.get(id=medicine_id)

        PrescriptionItem.objects.create(
            prescription=prescription,
            medicine=medicine,
            quantity=quantity
        )

        return JsonResponse({"message": "Prescription item added successfully"})
@csrf_exempt
def api_create_appointment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            patient = Patient.objects.get(id=data["patient_id"])
            doctor = Doctor.objects.get(id=data["doctor_id"])

            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=data["date"]
            )

            return JsonResponse({
                "message": "Appointment created successfully",
                "appointment_id": appointment.id
            })

        except Patient.DoesNotExist:
            return JsonResponse({"error": "Patient not found"}, status=404)

        except Doctor.DoesNotExist:
            return JsonResponse({"error": "Doctor not found"}, status=404)
@csrf_exempt
def api_create_prescription(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            appointment = Appointment.objects.get(id=data["appointment_id"])

            prescription = Prescription.objects.create(
                appointment=appointment
            )

            return JsonResponse({
                "message": "Prescription created successfully",
                "prescription_id": prescription.id
            })

        except Appointment.DoesNotExist:
            return JsonResponse({"error": "Appointment not found"}, status=404)                  