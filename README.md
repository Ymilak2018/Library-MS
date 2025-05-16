# Library-Management-System
Full‑stack Library Management System built with Django. Enables Students, Staff &amp; Faculty to self‑register, browse/request books, and manage returns via an intuitive dashboard. Includes automated email credentials, role‑based access control, real‑time activity tracking, admin CRUD for books/authors/subjects, request approvals, and stats.

## Library Management System

A simple and intuitive Library Management System built using pure Django Web Framework. This project streamlines library operations by providing separate interfaces for Students, Staff, Faculty, and Administrators.

---

## Requirement & Need

Managing a library manually can be time-consuming, error-prone, and inefficient. This system fulfills the following needs:

* **Automated User Onboarding**: New users can register and receive credentials automatically by email, reducing administrative overhead.
* **Secure Access Control**: Role-based access ensures that Students, Staff, and Faculty see only relevant features, while Administrators have full control.
* **Efficient Book Management**: Books can be added, updated, issued, and returned through a streamlined workflow, minimizing paperwork and delays.
* **Transparent Tracking**: All issue and return activities are logged and can be tracked in real-time, reducing loss and overdue returns.
* **Email Notifications**: Automatic emails inform users of approvals, denials, due dates, and password resets, improving communication and accountability.

---

## Key Features

### User Side (Student, Staff, Faculty)

1. **Registration & Login**

   * Sign up with role selection: Student, Staff, or Faculty.
   * Credentials (Library ID and password) emailed upon registration.
   * Login via username or Library ID.
2. **Password Recovery**

   * Forgot password flow with secure email link for reset.
3. **Dashboard**

   * View and edit profile (username, email, role).
   * Browse available books with search and filter.
   * Request book issuance and receive email confirmation or denial.
   * View issued books with photos, details, and return option.
   * Quick stats: total books borrowed, total issued books.
   * Logout button.

### Admin Side

1. **Admin Authentication**

   * Login via username, Library ID, or email.
   * Password reset via email.
2. **User Management**

   * View, update, and delete user profiles.
3. **Book & Catalogue Management**

   * Add, update, and delete books, authors, and subjects.
4. **Request & Activity Tracking**

   * Approve or decline book issue requests.
   * Track all borrowing activities: status (Returned, Not Returned, Due), borrower details.
   * Dashboard stats: total books, total borrowers, total registered users, recent activities.
   * Logout button.

---

## Tech Stack

* **Back-end:** Python, Django Web Framework
* **Templates:** Django Template Language (DTL)
* **Front-end:** HTML, CSS, JavaScript
* **Database:** SQLite (default) or configure to use PostgreSQL/MySQL
* **Email:** Django’s built-in email utilities (SMTP)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ymilak2018/Library-Management-System.git
   cd Library-Management-System
   ```
2. **Create & activate virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations & create superuser**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

## Usage

* Register a new user and choose a role.
* Log in to see the dashboard and manage books.
* As Admin, log in to add books, manage users, and track activities.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for:

* Bug fixes
* New features
* Documentation improvements

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For questions or support, contact `yashmilak20@gmail.com`.
