# Backend for Calendar Application for Communication 

## Overview

The backend of the Calendar Application for Communication is built using **Django** and **Django REST Framework**. It handles the business logic, data storage, and API endpoints to support the communication tracking functionalities in the application. The backend is structured into models, serializers, views, and URL routing to ensure clear separation of concerns and modularity.

---

## Components

### 1. **Models**

The models define the structure of the data and how it's stored in the database. There are three primary models in the backend:

#### **Company Model**

The `Company` model stores the information about companies involved in the communication process. It includes details such as the company name, location, LinkedIn profile, emails, phone numbers, comments, and the periodicity of communication (i.e., how often communication should happen).

**Fields**:
- `name`: The name of the company.
- `location`: The location of the company.
- `linkedin_profile`: The LinkedIn profile URL of the company.
- `emails`: A JSON field storing the list of emails associated with the company.
- `phone_numbers`: A JSON field storing the list of phone numbers associated with the company.
- `comments`: Additional comments about the company.
- `communication_periodicity`: The frequency at which communications should occur (in days). Default is 14 days.

#### **CommunicationMethod Model**

The `CommunicationMethod` model defines the various communication methods used in the application. This can include methods such as LinkedIn posts, email, phone calls, etc. Each communication method has an associated description, a sequence (which determines its priority), and a flag to specify if it is mandatory.

**Fields**:
- `name`: The name of the communication method (e.g., LinkedIn Post, Email).
- `description`: A detailed description of the communication method.
- `sequence`: A number indicating the priority or order of communication methods.
- `is_mandatory`: A boolean indicating whether this communication method is mandatory for a company.

#### **Communication Model**

The `Communication` model stores information about each individual communication with a company. It tracks the communication method, the date it occurred, any associated notes, the status (overdue, scheduled, or completed), and the due date of the communication.

**Fields**:
- `company`: A foreign key linking the communication to a specific company.
- `method`: A foreign key linking the communication to a specific communication method.
- `date`: The date the communication occurred.
- `notes`: Additional notes associated with the communication.
- `status`: The status of the communication (either 'overdue', 'completed', or 'scheduled').
- `due_date`: The due date for the communication to be performed.

The `save()` method in this model updates the status based on the due date and the current time:
- If the due date is in the past, the status is set to "overdue."
- If the due date is in the future, the status is set to "scheduled."
- If the due date is exactly the current time, the status is set to "completed."

---

### 2. **Serializers**

Serializers are used to convert the data from the models into a JSON format that can be used in API responses and also to parse incoming JSON data into model instances. The serializers define how each model’s data should be presented.

#### **CompanySerializer**

The `CompanySerializer` handles the serialization of the `Company` model. It also includes two additional fields:
- `lastFiveCommunications`: This field fetches the last five communications for a company.
- `nextScheduledCommunication`: This field fetches the next scheduled communication for the company.

#### **CommunicationMethodSerializer**

The `CommunicationMethodSerializer` serializes the `CommunicationMethod` model. It also renames the `name` field to `type` for consistency with the frontend.

#### **CommunicationSerializer**

The `CommunicationSerializer` serializes the `Communication` model. It includes:
- The primary key for the `Company` model.
- A nested serialization of the `CommunicationMethod` model to include details about the communication method.

---

### 3. **Views**

The views handle incoming HTTP requests, perform business logic, and return appropriate responses. In this application, we are using **Django REST Framework's viewsets**, which provide CRUD (Create, Read, Update, Delete) operations out of the box.

#### **CompanyViewSet**

The `CompanyViewSet` provides CRUD functionality for the `Company` model. It uses the `CompanySerializer` to serialize the data and provides endpoints for listing, retrieving, updating, and deleting companies.

#### **CommunicationMethodViewSet**

The `CommunicationMethodViewSet` provides CRUD functionality for the `CommunicationMethod` model. It uses the `CommunicationMethodSerializer` to serialize the data and provides endpoints for managing communication methods.

#### **CommunicationViewSet**

The `CommunicationViewSet` manages the communications between companies and tracks their status. It uses the `CommunicationSerializer` to serialize the data and provides the following actions:
- **Overdue Communications**: Fetches communications that are overdue.
- **Due Today Communications**: Fetches communications that are scheduled for today.

Additionally, custom filters are applied using query parameters:
- `overdue`: Filters communications that are overdue.
- `due-today`: Filters communications that are due today.

---

### 4. **URL Configuration**

The URL configuration defines how the application routes incoming requests to the appropriate views. It is set up in the `urls.py` file, where the backend API endpoints are registered.

#### **Example URL Setup**:

- `/admin/`: The Django admin interface to manage the application.
- `/admin-module/`: The endpoint for the admin module to manage companies and communication methods.
- `/user-module/`: The endpoint for the user module to manage communication tasks.
- `/reporting-module/`: The endpoint for generating reports.

---

### 5. **Admin**

The `admin.py` file registers the models in the Django admin interface to allow easy management of data. By registering the models, an admin user can manage companies, communication methods, and communications via the web interface.

**Registered Models**:
- `Company`
- `CommunicationMethod`
- `Communication`

---

### 6. **Authentication and Authorization**

The backend provides basic authentication mechanisms to secure access to the API. You can extend this by adding more complex authentication mechanisms, such as token-based authentication or OAuth, depending on the project requirements.

#### **User Model (for Admin/Regular Users)**

A `User` model is included to manage the users of the application. The `User` model stores:
- `username`: A unique identifier for the user.
- `email`: The user's email address.
- `password`: The user's password.
- `role`: Defines the role of the user (either 'Admin' or 'User').
- `is_active`: A flag to indicate whether the user's account is active.

---

## Future Enhancements

- **User Authentication**: Implement token-based authentication for better security and user management.
- **Reporting Module**: Add detailed reports on communication trends, frequency, and effectiveness.
- **Admin Panel Enhancements**: Add advanced filtering and reporting features for better management.
- **Real-Time Notifications**: Implement real-time notifications for overdue communications.

---

## Conclusion

This backend documentation provides a comprehensive overview of how the backend of the Calendar Application for Communication is structured. It covers the models, serializers, views, and the URL configuration, ensuring that developers and contributors can easily understand the system's architecture and how to extend or modify it. 