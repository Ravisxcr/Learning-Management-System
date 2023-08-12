# Learning Management System (LMS)


The Learning Management System (LMS) is a web application developed using Python, FastAPI, and MySQL. It provides an intuitive platform for educational institutions and organizations to manage and deliver online courses, track student progress, and facilitate collaboration between students and instructors.


## Tech Stack

- **Backend:** FastAPI, a modern, fast, web framework for building APIs with Python.

- **Database:** MySQL for storing user data, course content, and system information.

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ravisxcr/Learning-Management-System.git
   cd Learning-Management-System
   ```

2. Install dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database settings in `database.py`:
   ```python
   DATABASE_URL = "mysql://username:password@localhost/lms_db"
   ```


5. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

6. Access the LMS at `http://localhost:8000` in your web browser.
