# Student Question-and-Answer Platform

A premium, full-stack web application for student assessments, built with Python (Flask) and SQLite.

## Features

-   **Student Panel**: Register/Login, take quizzes (MCQ/Text), view real-time progress and history.
-   **Admin Panel**: View all student performance, export data to Excel (CSV) or SQL.
-   **Security**: Password hashing, session management.
-   **Design**: Modern, responsive UI with Glassmorphism effects and smooth animations.

## Tech Stack

-   **Frontend**: HTML5, Modern CSS3, Vanilla JavaScript.
-   **Backend**: Python, Flask.
-   **Database**: SQLite (No installation required).

## Installation & Setup

1.  **Helper Dependencies**:
    Ensure you have [Python 3](https://python.org/) installed on your system.
    Check with:
    ```bash
    python3 --version
    ```

2.  **Install Dependencies**:
    Open a terminal in this folder and run:
    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Initialize Database**:
    Before the first run, seed the database with admin and sample questions:
    ```bash
    python3 seed.py
    ```
    *This creates `database.sqlite` and adds an admin user + 5 sample questions.*

4.  **Run the Application**:
    ```bash
    python3 app.py
    ```
    The server will start at `http://localhost:3000`.

## Usage Guide

### 1. Student Access
-   Go to `http://localhost:3000`.
-   Click **Register** to create a new account, or login with the sample student:
    -   **Username**: `student`
    -   **Password**: `student123`
-   Navigate to **Dashboard** to see stats.
-   Click **Start New Quiz** to answer questions.

### 2. Admin Access
-   Login with the admin credentials:
    -   **Username**: `admin`
    -   **Password**: `admin123`
-   You will be redirected to the **Admin Dashboard**.
-   View student scores and click **Export** to download reports.
