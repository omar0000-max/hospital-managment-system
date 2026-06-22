from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    age = models.IntegerField(null=True, blank=True)          # NEW
    experience = models.IntegerField(null=True, blank=True)   # years

    def __str__(self):
        return self.name    
    
    def __str__(self):
        return self.name
    
        
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"
        
    
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 
    
    
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription {self.id}"  

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        # check stock
        if self.quantity > self.medicine.quantity:
            raise ValidationError("Not enough stock!")

        # reduce stock
        self.medicine.quantity -= self.quantity
        self.medicine.save()

        super().save(*args, **kwargs)