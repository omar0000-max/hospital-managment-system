# Hospital Management System (HMS)

A Simple Hospital Management System built with Django and SQLite to manage patients, doctors, appointments, prescriptions, and medical records. The system provides role-based access, appointment scheduling, prescription management, and inventory integration through REST APIs.

## Features

* Patient Management
* Doctor Management
* Appointment Scheduling
* Prescription Management
* Medical Records
* REST API Integration
* Inventory System Integration

## Technologies Used

* Python
* Django
* SQLite
* HTML, CSS
* Django REST Framework

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/hms.git
cd hms
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Apply migrations:

```bash
python manage.py migrate
```

6. Run the server:

```bash
python manage.py runserver
```

## Project Structure

* Patients Management
* Doctors Management
* Appointments Management
* Prescriptions Management
* REST API Services

## Future Improvements

* PostgreSQL Support
* Authentication & Authorization
* Inventory Management System
* Reports and Analytics
