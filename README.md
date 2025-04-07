# DTEAM - Django Developer Practical Test

Welcome! This test will help us see how you structure a Django project, work with various tools, and handle common tasks in web development. Follow the instructions step by step.

Good luck!

---

## Requirements

- Follow PEP 8 and other style guidelines.
- Use clear and concise commit messages and docstrings where needed.
- Structure your project for readability and maintainability.
- Optimize database access using Django's built-in methods.
- Provide enough details in your README.

---

## **Version Control System**

1. Create a **public GitHub repository** for this practical test, for example: `DTEAM-django-practical-test`.
2. Put the text of this test (all instructions) into `README.md`.
3. For each task, **create a separate branch** (for example, `tasks/task-1`, `tasks/task-2`, etc.).
4. When you finish each task, **merge that branch back into main** but do not delete the original task branch.

---

## **Python Virtual Environment**

1. Use **pyenv** to manage the Python version. Create a file named `.python-version` in your repository to store the exact Python version.
2. Use **Poetry** to manage and store project dependencies. This will create a `pyproject.toml` file.
3. Update your `README.md` with clear instructions on how to set up and use pyenv and Poetry for this project.

---

## **Tasks**

### **Task 1: Django Fundamentals**

1. **Create a New Django Project**
   - Name it something like `CVProject`.
   - Use the Python version set up in Task 2 and the latest stable Django release.
   - Use SQLite as your database for now.

2. **Create an App and Model**
   - Create a Django app (for example, `main`).
   - Define a `CV` model with fields like:
     - `firstname`
     - `lastname`
     - `skills`
     - `projects`
     - `bio`
     - `contacts`
   - Organize the data in a way that feels efficient and logical.

3. **Load Initial Data with Fixtures**
   - Create a fixture containing at least one sample `CV` instance.
   - Include instructions in `README.md` on how to load the fixture.

4. **List Page View and Template**
   - Implement a view for the main page (e.g., `/`) to display a list of CV entries.
   - Use any CSS library to style them nicely.
   - Ensure the data is retrieved from the database efficiently.

5. **Detail Page View**
   - Implement a detail view (e.g., `/cv/<id>/`) to show all data for a single CV.
   - Style it nicely and ensure efficient data retrieval.

6. **Tests**
   - Add basic tests for the list and detail views.
   - Update `README.md` with instructions on how to run these tests.

---

### **Task 2: PDF Generation Basics**

1. Choose and install any **HTML-to-PDF generating** library or tool.
2. Add a 'Download PDF' button on the CV detail page that allows users to download the CV as a PDF.

---

### **Task 3: REST API Fundamentals**

1. Install **Django REST Framework (DRF)**.
2. Create **CRUD endpoints** for the CV model (`create`, `retrieve`, `update`, `delete`).
3. Add tests to verify that each CRUD action works correctly.

---

### **Task 4: Middleware & Request Logging**

1. **Create a RequestLog Model**
   - You can put this in the existing app or a new app (e.g., `audit`).
   - Include fields such as:
     - `timestamp`
     - `HTTP method`
     - `path`
     - *Optionally* other details like query string, remote IP, or logged-in user.

2. **Implement Logging Middleware**
   - Write a custom Django middleware class that intercepts each incoming request.
   - Create a `RequestLog` record in the database with the relevant request data.
   - Keep it efficient.

3. **Recent Requests Page**
   - Create a view (e.g., `/logs/`) showing the **10 most recent logged requests**, sorted by `timestamp` descending.
   - Include a template that loops through these entries and displays their `timestamp`, `method`, and `path`.

4. **Test Logging**
   - Ensure your tests verify the logging functionality.

---

### **Task 5: Template Context Processors**

1. **Create `settings_context`**
   - Create a context processor that injects your entire Django settings into all templates.

2. **Settings Page**
   - Create a view (e.g., `/settings/`) that displays `DEBUG` and other settings values made available by the context processor.

---

### **Task 6: Docker Basics**

1. Use **Docker Compose** to containerize your project.
2. Switch the database from SQLite to **PostgreSQL** in Docker Compose.
3. Store all necessary environment variables (database credentials, etc.) in a `.env` file.

---

### **Task 7: Celery Basics**

1. Install and configure **Celery**, using Redis or RabbitMQ as the broker.
2. Add a Celery worker to your Docker Compose configuration.
3. On the CV detail page, add:
   - An email input field.
   - A 'Send PDF to Email' button to trigger a Celery task that emails the PDF.

---

### **Task 8: OpenAI Basics**

1. On the CV detail page, add a 'Translate' button and a language selector.
2. Include these languages:
   - Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino, Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian, Tsakonian, Saramaccan, Bislama.
3. Hook this up to an **OpenAI translation API** or any other translation mechanism you prefer.
4. The idea is to translate the CV content into the selected language.

---

### **Task 9: Deployment**

Deploy this project to DigitalOcean or any other VPS. *(If you do not have a DigitalOcean account, you can use this referral link to create an account with $200 on balance: [DigitalOcean Referral Link](https://m.do.co/c/967939ea1e74))*.

---

Complete each task thoroughly, commit your work following the branch-and-merge structure, and make sure your `README.md` clearly explains how to install, run, and test everything. We look forward to reviewing your submission!

---

**Thank you!**

# Setting Up the Project

## Requirements
Before proceeding, ensure you have the following installed on your machine:
- **Python** (compatible with this project's version)
- **pyenv**
- **Poetry**
- **SQLite** (default database for development)

---

## Setting Up Python with `pyenv`

To use the correct Python version for this project:

1. **Install pyenv**
   - Follow the [pyenv installation guide](https://github.com/pyenv/pyenv#installation) for your operating system.

2. **Install the required Python version**
   - Check the `.python-version` file in the repository for the version we are using (e.g., `3.x.x`).
   - Run:
     ```bash
     pyenv install <python-version>
     ```
   - Example:
     ```bash
     pyenv install 3.11.6
     ```

3. **Set the local Python version**
   - Ensure pyenv points to the correct Python version for this project. Run:
     ```bash
     pyenv local <python-version>
     ```
   - Example:
     ```bash
     pyenv local 3.11.6
     ```

4. **Verify the Python version**
   - Run:
     ```bash
     python --version
     ```
   - Ensure the output matches the version in the `.python-version` file.

---

## Setting Up the Project with `Poetry`

To manage dependencies and environment using Poetry:

1. **Install Poetry**
   - Follow the [official installation guide](https://python-poetry.org/docs/#installation).

2. **Install dependencies**
   - Navigate to the repository root and run:
     ```bash
     poetry install
     ```
     This will install all dependencies specified in the `pyproject.toml` file.

3. **Activate the virtual environment**
   Poetry creates a virtual environment for the project. To activate it, run:
   ```bash
   poetry shell
   ```

4. **Add new dependencies (if needed)**
   - Use Poetry's commands to add dependencies. Example:
     ```bash
     poetry add django
     ```

---

## Running Migrations and Preparing the Database

Once the environment is set up, you'll need to migrate the database:

1. Run the following command to execute migrations:
   ```bash
   python manage.py migrate
   ```

2. Verify that the database has been successfully migrated.

---

## Loading Initial Data from Fixtures

To load initial data (for example, a sample `CV` entry):

1. Ensure the database is set up and migrations are applied (as shown above).

2. Use the following command to load the fixture:
   ```bash
   python manage.py loaddata <fixture-file-name>.json
   ```
   Example:
   ```bash
   python manage.py loaddata cv.json
   ```

3. Verify the data is loaded by checking the database or accessing the relevant views in the app.

---

## Running the Development Server

To start the Django development server:

1. Run:
   ```bash
   python manage.py runserver
   ```

2. Open the browser and navigate to `http://127.0.0.1:8000/` to access the application.

---

## Running Tests

To run tests for the application:

1. Run the Django test suite using:
   ```bash
   python manage.py test
   ```

2. Ensure all tests pass before making changes or submitting your work.

---

By following these steps, you will be able to set up the project, manage dependencies, and load initial data into the database without issues.

## REST API Endpoints

- **List Users**: `GET /users/`
- **Retrieve User**: `GET /users/<id>/`
- **Create User**: `POST /users/`
  Example:
  ```
  {
      "first_name": "Jane",
      "last_name": "Doe"
  }
  ```
- **Update User**: `PATCH /users/<id>/`
  Example:
  ```
  {
      "first_name": "Johnathan"
  }
  ```
- **Delete User**: `DELETE /users/<id>/`
