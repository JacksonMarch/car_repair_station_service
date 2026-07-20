# Car Repair Station Service

## Project Overview
This application is a professional management tool designed for car service stations. It streamlines daily operations for service advisors and master technicians by providing a centralized system to track vehicle maintenance, technician assignments, and service history.

## Problems Solved
*   **Operational Inefficiency:** Eliminated manual tracking of vehicle service status and technician workload.
*   **Resource Allocation:** Resolved issues with assigning multiple technicians to complex jobs through a Many-to-Many relationship structure.
*   **Data Organization:** Transitioned from disorganized paper/manual logs to a structured, searchable database of clients, vehicles, and repair history.
*   **Archive Management:** Successfully implemented an archival system to maintain a clean workspace for active tasks while preserving historical records.

## Technical Implementation & Challenges
### Challenges Faced:
*   **Database Refactoring:** Transitioned from simple foreign key relationships to complex Many-to-Many fields for technicians and order types, which required significant database migrations and query refactoring.
*   **ORM Optimization:** Faced challenges with `FieldError` exceptions when migrating to `ManyToManyField`, requiring adjustments to `get_queryset` and usage of `prefetch_related` for performance.
*   **Data Integrity:** Encountered issues with state consistency (e.g., archived orders appearing in active lists), which was resolved by ensuring strict filter application in views and templates.

### What I Learned:
*   Deepened my understanding of **Django ORM**, specifically handling `ManyToManyField` and `Prefetch` objects to optimize database queries.
*   Mastered the implementation of **annotations and aggregations** to perform data calculations directly at the database level.
*   Improved my ability to debug complex field resolution errors and structure data models for real-world automotive workflows.
*   Gained practical experience in building **custom authentication forms and logic**, ensuring secure and user-friendly access to the system.
*   Learned to design and implement **custom Django forms**, providing a clean and efficient way to handle user input and data validation.
*   **Full Bootstrap 5 Integration:** Transitioned from writing custom CSS to utilizing a modern framework for a cleaner, faster UI.
*   **Utility-First Design:** Learned to build responsive, visually appealing interfaces using Bootstrap's utility classes (flexbox, spacing, shadows) without cluttering stylesheets.
*   **Frontend-Backend Synergy:** Successfully integrated `django-crispy-forms` with `crispy-bootstrap5` to automatically render beautifully styled forms for authentication and CRUD operations.
*   **CRM UX/UI Patterns:** Gained experience designing professional dashboards using Cards, organizing data in tables with integrated search and status Badges, and building safe deletion confirmation flows.

## Installation Instructions
### Prerequisites
*   Python 3.10+
*   Django 6.0+
*   Database (SQLite is configured by default)

### Steps
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/JacksonMarch/car_repair_station_service/](https://github.com/JacksonMarch/car_repair_station_service/)
    cd car_repair_station_service
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run migrations:**
    To set up the database structure, run:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```
5.  **Start the development server:**
    ```bash 
    python manage.py runserver
    ```
6.  **Access the application:**
    Open `http://127.0.0.1:8000/` in your browser.

## Database Visualization
The system architecture follows a structured model approach to handle complex relationships between technicians, service types, and orders. (See diagram in documentation).