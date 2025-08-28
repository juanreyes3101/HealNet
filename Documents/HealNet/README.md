

# HealNet

### Healthcare & Appointment Management Platform



## Table of Contents

1. [Introduction](#introduction)
2. [Purpose](#purpose)
3. [System Overview](#system-overview)
4. [Roles and Features](#roles-and-features)
5. [System Architecture](#system-architecture)
6. [Key Components](#key-components)
7. [Features](#features)
8. [Layered Architecture](#layered-architecture)
9. [Interaction Flowcharts](#interaction-flowcharts)
10. [Database](#database-schema)
11. [Technologies and Tools](#technologies-and-tools)
12. [Future Enhancements](#future-enhancements)
13. [License](#license)



## Introduction

**HealNet** is a web-based healthcare platform designed to simplify and digitalize medical appointment management. The platform connects patients, doctors, and healthcare providers (EPS), offering tools for appointment scheduling, medical profiles, and healthcare news/authorizations.

**HealNet** aims to improve accessibility and efficiency within the healthcare system by allowing patients to schedule and track appointments, while doctors can manage their availability and EPS administrators can share updates and authorizations.

This documentation provides developers with clear guidance on the system design, components, architecture, database schema, and technologies used to build and extend **HealNet**.



## Purpose

**HealNet’s purpose** is to enhance the healthcare experience by providing a modern, scalable, and user-friendly platform for managing appointments and improving patient-doctor interactions.

The platform empowers:

* **Patients**: Schedule, view, and manage appointments; view EPS updates; Profile settings.
* **Doctors**: Manage schedules, profile settings and track appointments.
* **EPS (Healthcare Providers)**: Publish announcements, share authorizations, and monitor patient-doctor interactions.



## System Overview

HealNet is a **full-stack web application** that combines an intuitive user interface with robust backend services.

Key features include:

* **User authentication & profiles** for patients, doctors, and admins.
* **Appointment scheduling system** with rescheduling and cancellation options.
* **News & forum module** where EPS can publish important updates.
* **Admin dashboard** for managing doctors, patients, and healthcare communications.

The system ensures **scalability, modularity, and security**, following a layered architecture to support future extensions like **telemedicine and calendar integration**.


## Roles and Features

* **Patients**:

  * Register, log in, and create personal profiles.
  * Schedule, view, reschedule, or cancel appointments.
  * View EPS updates and authorizations.

* **Doctors**:

  * Register and maintain professional profiles.
  * Manage availability and schedules.
  * View patient appointments.

* **EPS/Admins**:

  * Publish news, announcements, and authorizations.
  * Manage patient and doctor accounts.
  * Monitor system usage and engagement.


## System Architecture

HealNet follows a **modular, layered architecture** to ensure scalability, maintainability, and flexibility.

### **1️⃣ Frontend (Client-Side)**

* **Technologies:** HTML5, CSS3, JavaScript (React.js optional for scalability).
* **Responsibilities:**

  * Responsive and intuitive UI for patients and doctors.
  * Appointment scheduling interface.
  * Profile and dashboard management.
  * News & forum display.

### **2️⃣ Backend (Server-Side)**

* **Technologies:** Node.js, Express.js (alternatives: Django or Flask).
* **Responsibilities:**

  * Business logic (appointments, profiles, authorizations).
  * API endpoints for frontend communication.
  * Authentication and authorization.
  * Appointment validation and conflict management.

### **3️⃣ Database Layer**

* **Relational (PostgreSQL/MySQL):** Best for structured appointment and user data.
* **Responsibilities:** Store patients, doctors, appointments, and news updates.

### **4️⃣ Authentication & Security**

* JWT for secure login and session management.
* Password encryption with Bcrypt.js.
* HTTPS & SSL for secure communications.
* Role-based access control (Patient, Doctor, Admin).

### **5️⃣ Deployment & Version Control**

* **Version Control:** Git + GitHub.
* **Deployment:** Vercel/Render/Heroku for development; AWS/GCP/Azure for production.


## Key Components

* **User Authentication**: Role-based login and registration (Patient, Doctor, Admin).
* **Appointment Management**: CRUD operations for appointments.
* **News/Forum Module**: EPS publishes updates, visible to all users.
* **Profile Management**: Patient and doctor information dashboards.
* **Admin Panel**: Centralized control for EPS admins.


## Features

* Secure user authentication and profile creation.
* Appointment scheduling with notifications and reminders.
* Doctor schedule management.
* EPS forum for healthcare news and authorizations.
* Admin panel for system oversight.
* Responsive design for mobile and desktop.


## Layered Architecture

### **1. Presentation Layer**

* **Technologies:** HTML, CSS, JavaScript (React optional).
* **Responsibilities:** User interface, responsive design, communication with backend.

### **2. Business Logic Layer**

* **Technologies:** Node.js, Express.js.
* **Responsibilities:** Appointment validation, profile updates, role-based logic.

### **3. Data Access Layer (DAO)**

* **Technologies:** Sequelize (SQL) or Mongoose (NoSQL).
* **Responsibilities:** CRUD operations for users, appointments, and news.

### **4. Database Layer**

* **Technologies:** PostgreSQL/MySQL or MongoDB.
* **Responsibilities:** Store and manage structured/unstructured healthcare data.


## Interaction Flowcharts

### **User Registration Flow**

1. User enters registration details.
2. Backend validates input and encrypts password.
3. Database stores user details.
4. JWT token generated for session.
5. User redirected to dashboard.

### **Appointment Scheduling Flow**

1. Patient selects date, doctor, and time.
2. Backend checks for conflicts.
3. Appointment stored in database.
4. Confirmation sent to patient and doctor.

### **EPS News Flow**

1. Admin publishes update in forum.
2. Database stores news post.
3. Patients and doctors can view in dashboard.


## Database Schema

### **Users** 👤

```json
{
  "_id": ObjectId,
  "name": String,
  "email": String,
  "password": String,
  "role": String, // ["patient", "doctor", "admin"]
  "profile": {
    "bio": String,
    "specialization": String,
    "appointments": [ObjectId]
  },
  "created_at": ISODate
}
```

### **Appointments** 📅

```json
{
  "_id": ObjectId,
  "patient_id": ObjectId,
  "doctor_id": ObjectId,
  "date": ISODate,
  "status": String // ["scheduled", "completed", "canceled"]
}
```

### **News/Forum** 📰

```json
{
  "_id": ObjectId,
  "title": String,
  "content": String,
  "author": ObjectId, // EPS admin
  "created_at": ISODate
}
```


## Technologies and Tools

* **Frontend:** HTML5, CSS3, JavaScript, TailwindCSS, React.js (optional).
* **Backend:** Node.js, Express.js.
* **Database:** PostgreSQL/MySQL (Relational) or MongoDB (NoSQL).
* **Authentication & Security:** JWT, Bcrypt.js, HTTPS/SSL.
* **Deployment:** Vercel, Render, AWS, Heroku.
* **Version Control:** Git & GitHub.
* **Design Tools:** Figma (UI/UX).


## Future Enhancements

1. **Telemedicine module** with video calls.
2. **Integration with Google Calendar/Outlook**.
3. **Push/email notifications** for reminders.
4. **Payment & billing system** integration.
5. **Advanced analytics dashboards** for EPS.
6. **Mobile app** for iOS and Android.
7. **AI Chatbot** for EPS


## License

This project is licensed under the MIT License – see the LICENSE file for details.


