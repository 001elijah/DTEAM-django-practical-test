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
- **Redis**
- **PostgreSQL**
- **weasyprint** (install globally)

---

## To build and run the app locally `.env.local` should be created:

```aiignore
# Django environment
DEBUG=True
SECRET_KEY=django-insecure--h3@n&eq-m8=mgyub2yk7pnmkcm2k$0i11jpqnqrmc=q02_vv9

# PostgreSQL configuration
POSTGRES_DB=cvproject_db
POSTGRES_USER=cv_user
POSTGRES_PASSWORD=cv_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Email service variables
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
FROM_EMAIL=email@example.com
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

## Run Redis

## Run Celery within .venv (`CVProject` project name is case-sensitive)

```aiignore
celery -A CVProject worker --loglevel=info
```

## Run PostgreSQL DB

1. Start PostgreSQL database server
2. Start PostgreSQL database
3. Make sure the DB has a user `cv_user` with password `cv_password`

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
   source .venv/bin/activate
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
   export ENVIRONMENT=development
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

# Default Accounts

The system includes two default accounts created during the initial migrations for testing or development purposes. Details of these accounts are as follows:

### Admin Account
- **Username**: `admin`
- **Email**: `admin@admin.com`
- **Password**: `12345qwe`
- **Permissions**: Superuser with full administrative rights.

### Regular User Account
- **Username**: `user`
- **Email**: `user@user.com`
- **Password**: `12345qwe`
- **Permissions**: Regular user without staff or superuser rights.

> **Note:** These accounts are initialized as part of the `0007_auto_20250407_1921` database migration. You should update or remove these accounts in a production environment to ensure security.

# Pre-Commit Hooks and Lint Fixing

Pre-commit hooks are scripts or commands that are run automatically before a new commit is recorded in your repository. These hooks help ensure that certain code quality checks or formatting rules are adhered to, reducing errors and improving code consistency.

## Using Pre-Commit Hooks

The `pre-commit` framework is widely used to manage pre-commit hooks. The usual workflow involves defining the hooks in a `.pre-commit-config.yaml` file and installing them in your repository.

### Running Pre-Commit Hooks

To run pre-commit hooks on all files (not just staged files), use the following command:

```bash
pre-commit run --all-files
```

This command will execute all the hooks defined in the `.pre-commit-config.yaml` file across the entire codebase. It is helpful when you want to ensure your codebase complies with the rules even for files not part of the current commit.

### Sample `.pre-commit-config.yaml`

Here is an example configuration for pre-commit hooks that enforce formatting (with **Black, Isort, and Autoflake**) and linting (with **Flake8**):

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 7.2.0
    hooks:
      - id: flake8
        args: [ "--max-line-length=88" ]
  - repo: https://github.com/timothycrosley/isort
    rev: 6.0.1
    hooks:
      - id: isort
  - repo: https://github.com/myint/autoflake
    rev: v2.3.1
    hooks:
      - id: autoflake
        args: [ "--remove-all-unused-imports", "--remove-unused-variables", "-r" ]
```

To install these hooks in your project, run:

```bash
pre-commit install
```

This ensures that all the configured hooks will run automatically before each commit.

---

## Fixing Lint Issues with Poetry

To fix linting and formatting issues quickly across your codebase, you can use a custom script together with Poetry. A good example is the `lint_fix.py` script. It automates running tools like Autoflake, Isort, and Black to apply fixes.

### Script for Lint Fixing

The script (`lint_fix.py`) can execute necessary commands sequentially, such as removing unused imports, sorting imports, and applying consistent code formatting.

Here is an example:

```python
import subprocess

def main():
    """Runs all the necessary lint fix steps."""
    commands = [
        # Autoflake: Removes unused imports and variables
        "autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .",  # noqa: E501
        # isort: Sort imports
        "isort .",
        # Black: Format code
        "black .",
    ]

    for command in commands:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True)
```

---

### Quick Lint Fix Using Poetry

To run the script with Poetry, you can use the following command:

```bash
poetry run lint-fix
```

This will execute the `lint_fix.py` script and apply Autoflake, Isort, and Black fixes to the entire project.

---

## Summary of Commands

Below are the key commands covered:

1. **Run pre-commit hooks on all files**:
   ```bash
   pre-commit run --all-files
   ```

2. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

3. **Quickly apply fixes with Poetry**:
   ```bash
   poetry run lint-fix
   ```

Using these tools together ensures your code stays clean, consistent, and compliant with coding standards.

# REST API Endpoints

## API: User Authentication and Registration

This section describes routes for user registration, token generation, and token refresh to enable user authentication.

### Available Functionality

| Functionality                | Description                                                                             |
|------------------------------|-----------------------------------------------------------------------------------------|
| User Registration            | Register a new user in the system.                                                     |
| Obtain Token                 | Generate access and refresh tokens by providing valid credentials.                     |
| Refresh Token                | Obtain a new access token by providing a valid refresh token.                          |

### Endpoints

- **`POST /api/register/`**: Register a new user.
- **`POST /api/token/`**: Obtain access and refresh tokens.
- **`POST /api/token/refresh/`**: Refresh the access token.

---

### Example cURL Requests and Responses

#### 1. **User Registration**

Register a new user by sending the username, password, and email.

```bash
curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{
  "username": "test",
  "password": "12345qwe",
  "email": "test@test.com"
}'
```

**Example Response**:
```json
{
  "message": "User registered successfully!"
}
```

---

#### 2. **Obtain Token**

Log in using valid credentials (username and password) to retrieve the access and refresh tokens.

```bash
curl -X POST http://localhost:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{
  "username": "test",
  "password": "12345qwe"
}'
```

**Example Response**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDIxODA3OCwiaWF0IjoxNzQ0MTMxNjc4LCJqdGkiOiJkMzBlOGQ0YzQ4NDg0OTEwOWY4NDM0YmE5YjU2YzE0MiIsInVzZXJfaWQiOjR9.KHgldx5dZkMn0aEGbp-q_v6_1TeF3EwUHzeFGbfxuKY",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTMxOTc4LCJpYXQiOjE3NDQxMzE2NzgsImp0aSI6ImNjYWZlYTI3YzljNjRmYWZiZGYxMzVjYTI5NTc5ZmU5IiwidXNlcl9pZCI6NH0.0PiIuB8gU_A0Z0gC4aXylI3ILQ8NKcBDcAPRS5PIcFI"
}
```

You can use the `access` token for authentication in secure endpoints and the `refresh` token to generate new access tokens when expired.

---

#### 3. **Invalid Credentials (Token Generation)**

If invalid credentials are provided during login, the response will indicate the failure.

```bash
curl -X POST http://localhost:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{
  "username": "test",
  "password": "wrongpassword"
}'
```

**Example Response**:
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

#### 4. **Refresh Access Token**

Use the refresh token to generate a new access token when the existing access token expires.

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
-H "Content-Type: application/json" \
-d '{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDIxODA3OCwiaWF0IjoxNzQ0MTMxNjc4LCJqdGkiOiJkMzBlOGQ0YzQ4NDg0OTEwOWY4NDM0YmE5YjU2YzE0MiIsInVzZXJfaWQiOjR9.KHgldx5dZkMn0aEGbp-q_v6_1TeF3EwUHzeFGbfxuKY"
}'
```

**Example Response**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTMxOTc4LCJpYXQiOjE3NDQxMzE2NzgsImp0aSI6ImNjYWZlYTI3YzljNjRmYWZiZGYxMzVjYTI5NTc5ZmU5IiwidXNlcl9pZCI6NH0.0PiIuB8gU_A0Z0gC4aXylI3ILQ8NKcBDcAPRS5PIcFI"
}
```

---

### Notes:

- **Authentication**:
  - After registration, users need to log in to get their `access` and `refresh` tokens.
  - Use the `Authorization` header with the `Bearer <access_token>` to access authenticated endpoints.
- **Tokens**:
  - The `access` token has a short lifespan and is used for accessing data.
  - The `refresh` token has a longer lifespan and is used to request new access tokens without requiring a login.
- **Error Handling**:
  - Proper error messages are returned for invalid users or tokens.


## API: Candidate Management

This API provides endpoints for managing **candidates**, including their detailed information.

### Available Functionality

| Functionality               | Description                                                                     |
|-----------------------------|---------------------------------------------------------------------------------|
| List All Candidates         | Retrieve a list of all candidates with their basic information.                 |
| Create a New Candidate      | Add a new candidate to the system by providing their details.                   |
| Retrieve a Specific Candidate by ID | Get detailed information about a specific candidate using their unique ID.   |
| Update an Existing Candidate | Modify the details of an existing candidate by providing their unique ID.       |
| Delete a Candidate          | Remove a candidate from the system using their unique ID.                      |

---

### Endpoints:

- **`GET /api/candidates/`**: Retrieve a list of all candidates.
- **`POST /api/candidates/`**: Add a new candidate.
- **`GET /api/candidates/{id}/`**: Retrieve details for a specific candidate by their unique ID.
- **`PUT /api/candidates/{id}/`**: Update details of an existing candidate.
- **`DELETE /api/candidates/{id}/`**: Delete a candidate by their unique ID.

---

### Example cURL Requests and Responses:

#### 1. **List All Candidates**
Retrieve a list of all candidates.

```bash
curl -X GET http://<your-domain>/api/candidates/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

**Example Response**:
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe"
  },
  {
    "id": 2,
    "first_name": "Jane",
    "last_name": "Smith"
  }
]
```

---

#### 2. **Create a New Candidate**
Create a new candidate by providing their details.

```bash
curl -X POST http://<your-domain>/api/candidates/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Johnson"
  }'
```

**Example Response**:
```json
{
  "id": 3,
  "first_name": "Alice",
  "last_name": "Johnson"
}
```

---

#### 3. **Retrieve a Specific Candidate by ID**
Retrieve a candidate's detailed information using their unique ID.

```bash
curl -X GET http://<your-domain>/api/candidates/1/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

**Example Response**:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe"
}
```

---

#### 4. **Update an Existing Candidate**
Update the details of an existing candidate.

```bash
curl -X PUT http://<your-domain>/api/candidates/1/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe Updated"
  }'
```

**Example Response**:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe Updated"
}
```

---

#### 5. **Delete a Candidate**
Delete a candidate using their unique ID.

```bash
curl -X DELETE http://<your-domain>/api/candidates/1/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

**Example Response**:
```json
{
  "message": "Candidate deleted successfully."
}
```

---

### Notes:

- **Authentication Required**: All endpoints require an authenticated user. Provide the `Authorization` header with a valid JWT token as `Bearer <your_token>`.
- **Fields**:
    - **`first_name`**: The first name of the candidate (string; required).
    - **`last_name`**: The last name of the candidate (string; required).
- **ID Placeholder**: Replace `{id}` in the endpoints with the unique ID of the candidate (e.g., `/api/candidates/1/`).

---

## API: Bio Item Management

This API provides endpoints to manage bio items associated with candidates in the system.

### Available Functionality

| Functionality                | Description                                                                             |
|------------------------------|-----------------------------------------------------------------------------------------|
| List All Bio Items           | Retrieve a list of all bio items associated with candidates.                           |
| Create a New Bio Item        | Add a new bio item for a specific candidate.                                           |
| Retrieve a Specific Bio Item by ID | Get detailed information about a specific bio item using its unique ID.              |
| Update an Existing Bio Item  | Modify the content or details of an existing bio item by providing its unique ID.      |
| Delete a Bio Item            | Remove a bio item using its unique ID.                                                 |

### Endpoints:

- **`GET /api/bio_items/`**: Retrieve a list of all bio items.
- **`POST /api/bio_items/`**: Create a new bio item.
- **`GET /api/bio_items/{id}/`**: Retrieve the details of a specific bio item.
- **`PUT /api/bio_items/{id}/`**: Update an existing bio item.
- **`DELETE /api/bio_items/{id}/`**: Delete a bio item.

### Example cURL Requests

1. **List All Bio Items**  
   ```bash
   curl -X GET http://<your-domain>/api/bio_items/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

2. **Create a New Bio Item**  
   ```bash
   curl -X POST http://<your-domain>/api/bio_items/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate": 1,
       "bio_item": "Experienced developer with expertise in REST APIs and frontend technologies."
     }'
   ```

3. **Retrieve a Bio Item by ID**  
   ```bash
   curl -X GET http://<your-domain>/api/bio_items/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

4. **Update a Bio Item**  
   ```bash
   curl -X PUT http://<your-domain>/api/bio_items/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate": 1,
       "bio_item": "Senior software engineer specializing in Django and backend integrations."
     }'
   ```

5. **Delete a Bio Item**  
   ```bash
   curl -X DELETE http://<your-domain>/api/bio_items/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

### Notes:

- **Authentication Required**: All endpoints require an authenticated user.
- **Authorization Header**: Include your valid JWT token in the `Authorization` header as `Bearer <your_token>`.
- **Fields**:
  - **`candidate`**: The ID of the candidate to whom the bio item belongs (integer; required).
  - **`bio_item`**: The content of the bio item (text; required, potentially new validation/fields depending on the updated serializer).

---

## API: Skill Management

This API provides endpoints to manage skills within the system.

### Endpoints:

- **`GET /api/skills/`**: Retrieve a list of all skills.
- **`POST /api/skills/`**: Create a new skill.
- **`GET /api/skills/{id}/`**: Retrieve the details of a specific skill.
- **`PUT /api/skills/{id}/`**: Update an existing skill.
- **`DELETE /api/skills/{id}/`**: Delete a skill.

### Example cURL Requests

1. **List All Skills**  
   ```bash
   curl -X GET http://<your-domain>/api/skills/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

2. **Create a New Skill**  
   ```bash
   curl -X POST http://<your-domain>/api/skills/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Django"
     }'
   ```

3. **Retrieve a Skill by ID**  
   ```bash
   curl -X GET http://<your-domain>/api/skills/3/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

4. **Update a Skill**  
   ```bash
   curl -X PUT http://<your-domain>/api/skills/3/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Django REST Framework"
     }'
   ```

5. **Delete a Skill**  
   ```bash
   curl -X DELETE http://<your-domain>/api/skills/3/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

### Notes:
- **Authentication Required:** All endpoints (except `GET /api/skills/`) require an authenticated user.  
- **Authorization Header:** Include your valid JWT token in requests as `Bearer <your_token>`.

---

## API: Candidate Skill Management

**Route**: `/api/candidate_skills/`  
**Methods Allowed**: `GET`, `POST`, `DELETE`
**Description**: This API manages the relationships between candidates and skills. A candidate can have multiple skills, and a skill can belong to multiple candidates.

### Available Functionality

| Method | Endpoint                      | Description                          |
|--------|-------------------------------|--------------------------------------|
| GET    | `/api/candidate_skills/`      | Retrieve all candidate-skill pairs. |
| POST   | `/api/candidate_skills/`      | Create a new candidate-skill pair.  |
| DELETE | `/api/candidate_skills/<id>/` | Delete a candidate-skill pair.      |


---

### Endpoints

#### 1. **GET** `/api/candidate_skills/`
Fetches the list of candidate-skill relationships.

**Response Example**:
```json
[
    {
        "id": 1,
        "skill": {
            "id": 1,
            "skill_name": "Python"
        },
        "candidate": 1
    },
    {
        "id": 2,
        "skill": {
            "id": 2,
            "skill_name": "Django"
        },
        "candidate": 1
    }
]
```

---

#### 2. **POST** `/api/candidate_skills/`
Creates a new candidate-skill relationship.

**Request Example**:
```json
{
    "skill": {
        "skill_name": "JavaScript"
    },
    "candidate": 2
}
```

**Response Example**:
```json
{
    "id": 3,
    "skill": {
        "id": 3,
        "skill_name": "JavaScript"
    },
    "candidate": 2
}
```

**Notes**:
- The `candidate` field is required and should reference the candidate's ID.
- The `skill` field requires the `skill_name`. If the skill does not exist, it will be created automatically.

---

#### 3. **DELETE** `/api/candidate_skills/<id>/`
Deletes an existing candidate-skill relationship by its ID.

**Response Example**:
- On success:
```
HTTP 204 No Content
Allow: GET, DELETE
Content-Type: application/json
Vary: Accept

{
    "detail": "CandidateSkill and orphaned Skill (if any) deleted."
}
```

---

### Error Handling

- **405 Method Not Allowed**  
  Returned when using unsupported methods (e.g., `PUT` or `PATCH`).

- **400 Bad Request**  
  Returned for invalid request payloads. For example:
  ```json
  {
      "error": "Invalid data received."
  }
  ```

- **404 Not Found**  
  Returned when trying to access or delete a candidate-skill relationship that does not exist.

---

### Features

- **Candidate Reference by ID**: The API requires only the candidate's `id` for creating relationships.
- **Dynamic Skill Creation**: If the specified `skill_name` does not exist, it will be automatically created.
- **Minimal Data Input**: Only the `candidate` ID and `skill_name` are needed for POST requests.

---

### Example cURL Requests

#### 1. **Fetch All Candidate Skills (GET)**:
```bash
curl -X GET http://127.0.0.1:8000/api/candidate_skills/ \
-H "Authorization: Bearer <your_token>"
```

#### 2. **Create a New Candidate Skill (POST)**:
```bash
curl -X POST http://127.0.0.1:8000/api/candidate_skills/ \
-H "Authorization: Bearer <your_token>" \
-H "Content-Type: application/json" \
-d '{
    "skill": {
        "skill_name": "JavaScript"
    },
    "candidate": 2
}'
```

#### 3. **Delete a Candidate Skill (DELETE)**:
```bash
curl -X DELETE http://127.0.0.1:8000/api/candidate_skills/3/ \
-H "Authorization: Bearer <your_token>"
```

---

## API: Project Management

This API provides endpoints to manage projects within the system.

### Available Functionality

| Functionality                            | Description                                                                           |
|------------------------------------------|---------------------------------------------------------------------------------------|
| List All Projects                        | Retrieve a list of all available projects.                                            |
| Create a New Project                     | Add a new project with a name and description.                                        |
| Retrieve a Specific Project by ID        | Get detailed information about a specific project using its unique ID.                |
| Update an Existing Project               | Modify the name or description of an existing project by providing its unique ID.     |
| Delete a Project                         | Remove a project from the system using its unique ID.                                 |

### Endpoints:

- **`GET /api/projects/`**: Retrieve a list of all projects.
- **`POST /api/projects/`**: Create a new project.
- **`GET /api/projects/{id}/`**: Retrieve the details of a specific project.
- **`PUT /api/projects/{id}/`**: Update an existing project.
- **`DELETE /api/projects/{id}/`**: Delete a project.

### Example cURL Requests

1. **List All Projects**  
   ```bash
   curl -X GET http://<your-domain>/api/projects/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

2. **Create a New Project**  
   ```bash
   curl -X POST http://<your-domain>/api/projects/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "project_name": "Portfolio Website",
       "project_description": "A website to showcase personal portfolio and projects."
     }'
   ```

3. **Retrieve a Project by ID**  
   ```bash
   curl -X GET http://<your-domain>/api/projects/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

4. **Update a Project**  
   ```bash
   curl -X PUT http://<your-domain>/api/projects/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "project_name": "Updated Portfolio Website",
       "project_description": "An updated description for the portfolio website project."
     }'
   ```

5. **Delete a Project**  
   ```bash
   curl -X DELETE http://<your-domain>/api/projects/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

### Notes:

- **Authentication Required**: All endpoints require an authenticated user. 
- **Authorization Header**: Include your valid JWT token in the `Authorization` header as `Bearer <your_token>`.
- **Fields**:
  - **`project_name`**: The name of the project (string; required and unique).
  - **`project_description`**: A detailed description of the project (text; required).

---

## API: Candidate Project Management

This API allows you to manage associations between **candidates** and their respective **projects**.

---

### Available Functionality

| Functionality                    | Description                                                                     |
|----------------------------------|---------------------------------------------------------------------------------|
| List Candidate's Projects        | Retrieve a list of all projects associated with candidates.                     |
| Add a Project to a Candidate     | Add a new project or associate an existing project to a candidate.              |
| Delete a Candidate's Project     | Remove a project association for a specific candidate.                          |

**Note:** Only `GET`, `POST`, and `DELETE` HTTP methods are allowed for these routes.

---

### Endpoints:

- **`GET /api/candidate_projects/`**: Retrieve a list of all candidate-project associations.
- **`POST /api/candidate_projects/`**: Create a new project and associate it with a candidate, or directly associate an existing project.
- **`DELETE /api/candidate_projects/{id}/`**: Remove a project association for a candidate.

---

### Example cURL Requests and Responses:

#### 1. **List Candidate's Projects**
Retrieve all associations of candidates and their respective projects.

```bash
curl -X GET http://localhost:8000/api/candidate_projects/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

**Example Response**:
```json
[
  {
    "id": 1,
    "project": {
      "id": 1,
      "project_name": "Portfolio Website",
      "project_description": "A personal portfolio website showcasing my work and skills."
    },
    "candidate": 1
  },
  {
    "id": 2,
    "project": {
      "id": 2,
      "project_name": "Inventory Management System",
      "project_description": "A system for real-time inventory tracking."
    },
    "candidate": 2
  }
]
```

---

#### 2. **Add a Project to a Candidate**
Create a new project while associating it with a candidate or directly associate an existing project.

```bash
curl -X POST http://localhost:8000/api/candidate_projects/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "project": {
      "project_name": "New Project Name",
      "project_description": "Detailed description of the project."
    },
    "candidate": 3
  }'
```

**Example Response**:
```json
{
  "id": 10,
  "candidate": 3,
  "project": {
    "id": 7,
    "project_name": "New Project Name",
    "project_description": "Detailed description of the project."
  }
}
```

---

#### 3. **Delete a Candidate's Project**
Remove an association between a candidate and a project using the candidate-project relationship's ID.

```bash
curl -X DELETE http://localhost:8000/api/candidate_projects/10/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json"
```

**Example Response**:
```json
{
  "message": "Candidate project deleted successfully."
}
```

---

### Notes:

- **Authentication Required**: All API endpoints require an authenticated user. Provide the `Authorization` header with a valid JWT token as `Bearer <your_token>`.
- **Fields**:
  - **`project`:** The project object with:
    - **`project_name`**: The name of the project (string; required).
    - **`project_description`**: A detailed description of the project (string; required).
  - **`candidate`:** The unique ID of the candidate associated with the project (integer; required).
- **ID Placeholder**: Replace `{id}` in the DELETE endpoint with the unique ID of the candidate-project association (e.g., `/api/candidate_projects/10/`).

---

## API: Contact Management

This API provides endpoints to manage candidate contacts in the system.

### Available Functionality

| Functionality                | Description                                                                             |
|------------------------------|-----------------------------------------------------------------------------------------|
| List All Contacts            | Retrieve a list of all contacts associated with candidates.                            |
| Create a New Contact         | Add a new contact for a candidate, specifying the contact type and details.            |
| Retrieve a Specific Contact by ID | Get detailed information about a specific contact using its unique ID.              |
| Update an Existing Contact   | Modify the details of an existing contact by providing its unique ID.                  |
| Delete a Contact             | Remove a contact using its unique ID.                                                  |

### Endpoints:

- **`GET /api/contacts/`**: Retrieve a list of all candidate contacts.
- **`POST /api/contacts/`**: Create a new candidate contact.
- **`GET /api/contacts/{id}/`**: Retrieve the details of a specific contact.
- **`PUT /api/contacts/{id}/`**: Update an existing candidate contact.
- **`DELETE /api/contacts/{id}/`**: Delete a contact.

### Example cURL Requests

1. **List All Contacts**  
   ```bash
   curl -X GET http://<your-domain>/api/contacts/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

2. **Create a New Contact**  
   ```bash
   curl -X POST http://<your-domain>/api/contacts/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate": 1,
       "contact": "example@example.com",
       "contact_type": 2
     }'
   ```

3. **Retrieve a Contact by ID**  
   ```bash
   curl -X GET http://<your-domain>/api/contacts/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

4. **Update a Contact**  
   ```bash
   curl -X PUT http://<your-domain>/api/contacts/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate": 1,
       "contact": "new_email@example.com",
       "contact_type": 3
     }'
   ```

5. **Delete a Contact**  
   ```bash
   curl -X DELETE http://<your-domain>/api/contacts/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

### Notes:

- **Authentication Required**: All endpoints require an authenticated user.
- **Authorization Header**: Include your valid JWT token in the `Authorization` header as `Bearer <your_token>`.
- **Fields**:
  - **`candidate`**: The ID of the candidate to whom the contact belongs (integer; required).
  - **`contact`**: The actual contact details, such as an email or phone number (string; required, unique).
  - **`contact_type`**: The type/category of the contact (e.g., email, phone) (integer; required).

## API: Contact Type Management

This API provides endpoints to manage contact types in the system. A **contact type** defines the category of a contact (e.g., "Email", "Phone", etc.).

### Available Functionality

| Functionality                | Description                                                                             |
|------------------------------|-----------------------------------------------------------------------------------------|
| List All Contact Types       | Retrieve a list of all contact types available in the system.                          |
| Create a New Contact Type    | Add a new contact type (e.g., "Email", "Phone").                                       |
| Retrieve a Specific Contact Type by ID | Get detailed information about a specific contact type using its unique ID.       |
| Update an Existing Contact Type | Modify the details of an existing contact type by providing its unique ID.            |
| Delete a Contact Type        | Remove a contact type using its unique ID.                                             |

### Endpoints:

- **`GET /api/contact_types/`**: Retrieve a list of all contact types.
- **`POST /api/contact_types/`**: Create a new contact type (e.g., email, phone).
- **`GET /api/contact_types/{id}/`**: Retrieve the details of a specific contact type.
- **`PUT /api/contact_types/{id}/`**: Update an existing contact type.
- **`DELETE /api/contact_types/{id}/`**: Delete a contact type.

### Example cURL Requests

1. **List All Contact Types**  
   ```bash
   curl -X GET http://<your-domain>/api/contact_types/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

2. **Create a New Contact Type**  
   ```bash
   curl -X POST http://<your-domain>/api/contact_types/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "contact_type": "Email"
     }'
   ```

3. **Retrieve a Contact Type by ID**  
   ```bash
   curl -X GET http://<your-domain>/api/contact_types/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

4. **Update a Contact Type**  
   ```bash
   curl -X PUT http://<your-domain>/api/contact_types/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "contact_type": "Updated Contact Type"
     }'
   ```

5. **Delete a Contact Type**  
   ```bash
   curl -X DELETE http://<your-domain>/api/contact_types/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

### Notes:

- **Authentication Required**: All endpoints require an authenticated user.
- **Authorization Header**: Include your valid JWT token in the `Authorization` header as `Bearer <your_token>`.
- **Fields**:
  - **`contact_type`**: The name of the contact type (e.g., Email, Phone) (string; required, unique).

## API: Candidate Summary Management

This API provides endpoints to manage **candidate summaries**, which include aggregated information about a candidate such as their bio, skills, projects, and contacts.

### Available Functionality

| Functionality                | Description                                                                             |
|------------------------------|-----------------------------------------------------------------------------------------|
| List All Candidate Summaries | Retrieve a list of all summaries for candidates.                                       |
| Retrieve a Specific Candidate Summary by ID | Get detailed information about a specific candidate summary using its unique ID. |

### Endpoints:

- **`GET /api/candidate_summaries/`**: Retrieve a list of all candidate summaries.

### Example cURL Requests

1. **List All Candidate Summaries**  
   ```bash
   curl -X GET http://<your-domain>/api/candidate_summaries/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```
2. **Retrieve a Candidate Summary by ID**  
   ```bash
   curl -X GET http://<your-domain>/api/candidate_summaries/1/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json"
   ```

### Notes:

- **Authentication Required**: All endpoints require an authenticated user.
- **Authorization Header**: Include your valid JWT token in the `Authorization` header as `Bearer <your_token>`.
- **Fields**:
  - **`candidate`**: The ID of the candidate to whom the summary belongs (integer; required).
  - **`bio`**: The biography of the candidate (string; optional).
  - **`skills`**: A list of skill IDs associated with the candidate (array of integers; optional).
  - **`projects`**: A list of project IDs associated with the candidate (array of integers; optional).
  - **`contacts`**: A list of contact IDs associated with the candidate (array of integers; optional).

# Example Candidate Management API Workflow

This document describes the workflow for managing candidates using the API endpoints. It includes steps for creating a candidate, adding biography items, skills, projects, and contacts, and deleting a candidate. Examples are provided with detailed descriptions and realistic data.

---

## Workflow Steps

### Step 1: Create a Candidate

Create a candidate with relevant personal details like `first_name` and `last_name`.

**Endpoint:**  
`POST http://127.0.0.1:8000/api/candidates/`

**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response:**
```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 7,
    "first_name": "John",
    "last_name": "Doe"
}
```

---

### Step 2: Add Biography Item for Candidate

Add a biography entry to the candidate to describe their background or achievements.

**Endpoint:**  
`POST http://127.0.0.1:8000/api/bio_items/`

**Request Body:**
```json
{
    "bio_item": "Experienced software engineer with a focus on backend development and APIs.",
    "candidate": 7
}
```

**Response:**
```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 8,
    "bio_item": "Experienced software engineer with a focus on backend development and APIs.",
    "candidate": 7
}
```

---

### Step 3: Add Skills to Candidate

Associate skills the candidate has, such as programming languages or tools they are proficient in.

**Endpoint:**  
`POST http://127.0.0.1:8000/api/candidate_skills/`

**Request Body:**
```
{
    "skill": 1,
    "candidate": 7
}
```

Here, `skill: 1` corresponds to a skill (e.g., Python), pre-existing in your database.

**Response:**
```
HTTP 201 Created
Allow: GET, POST
Content-Type: application/json
Vary: Accept

{
    "id": 53,
    "skill": 1,
    "candidate": 7
}
```

---

### Step 4: Assign a Project to Candidate

Assign a project that the candidate has worked on. Provide comprehensive details about the project.

**Endpoint:**  
`POST http://127.0.0.1:8000/api/candidate_projects/`

**Request Body:**
```
{
    "project": {
        "project_name": "E-Commerce Platform Development",
        "project_description": "Designed and implemented the backend for an e-commerce platform allowing real-time inventory updates and secure payment integration."
    },
    "candidate": 7
}
```

**Response:**
```
HTTP 201 Created
Allow: GET, POST
Content-Type: application/json
Vary: Accept

{
    "id": 17,
    "project": {
        "id": 15,
        "project_name": "E-Commerce Platform Development",
        "project_description": "Designed and implemented the backend for an e-commerce platform allowing real-time inventory updates and secure payment integration."
    },
    "candidate": 7
}
```

---

### Step 5: Add Contact Information for Candidate

Add contact details for the candidate, such as their email address or phone number. Select the `contact_type` from predefined options (e.g., 1 = Email, 2 = Phone).

**Endpoint:**  
`POST http://127.0.0.1:8000/api/contacts/`

**Request Body:**
```
{
    "candidate": 7,
    "contact_type": 1,
    "contact": "john.doe@example.com"
}
```

**Response:**
```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 12,
    "candidate": 7,
    "contact_type": 1,
    "contact": "john.doe@example.com"
}
```

---

### Step 6: Delete a Candidate

Remove a candidate from the system, including all associated records like biography items, skills, projects, and contact details.

**Endpoint:**  
`DELETE http://127.0.0.1:8000/api/candidates/7/`

**Response:**
```
HTTP 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```

---

## Summary

This workflow ensures efficient handling of candidate records:

1. **Create Candidate:** Add a new candidate with personal details.
2. **Add Biography Items:** Enrich candidate profiles with background and achievements.
3. **Add Skills:** Associate skills that align with the candidate's expertise.
4. **Assign Projects:** Document projects the candidate has worked on.
5. **Add Contact Information:** Record candidate contact details for communication.
6. **Delete Candidate:** Remove a candidate and associated data when no longer needed.

For more detailed information, refer to the API documentation or the backend implementation. This guide serves to clarify how API endpoints are used to manage candidate-related data efficiently.

---

# Request Logging and Recent Logs

- **Middleware**: Automatically logs details for every HTTP request made to the application.
  - Logs include: HTTP Method, Path, Query String, IP Address, User Agent, and the User (if authenticated).
- **Recent Logs**: View the 10 most recent HTTP requests at `/audit/logs/`.

---

# Run Docker

To build and run Docker container `.env.production` should be created:
```aiignore
   # Django environment
DEBUG=True
SECRET_KEY=django-insecure--h3@n&eq-m8=mgyub2yk7pnmkcm2k$0i11jpqnqrmc=q02_vv9

# PostgreSQL configuration
POSTGRES_DB=cvproject_db
POSTGRES_USER=cv_user
POSTGRES_PASSWORD=cv_password
POSTGRES_HOST=db #should be the same as db service name in docker-compose.yml
POSTGRES_PORT=5432

CELERY_BROKER_URL = 'redis://redis:6379/0' #should be the same as redis service name in docker-compose.yml

# Email service variables
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
FROM_EMAIL=email@example.com
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```
```bash
docker-compose build
```

```bash
docker-compose up
```

To load the initial data fixture (`cv.json`) into the database, use the following command:

```bash
docker-compose exec web python manage.py loaddata main/fixtures/cv.json
```

This command should only be run **after the services are up and the database is ready**.
