

# API Hyperativa

This project is a Flask application designed to run inside a Docker container. It uses Waitress to serve the app and SQLite as the database. The application includes user authentication and card management functionalities.

## Requirements

- Docker
- Python 3.11
- pip

## Step-by-Step Setup Guide

### Step 1: Build the Docker Image

First, you need to build the Docker image for the application:

```bash
docker build -t api-hyperativa .
```

### Step 2: Initialize the Database

Before running the application for the first time, you need to set up the database:

1. Run a bash shell inside the Docker container:

    ```bash
    docker run -it api-hyperativa bash
    ```

2. Initialize the database:

    ```bash
    python manage.py db init
    python manage.py db migrate -m "Initial migration."
    python manage.py db upgrade
    ```

### Step 3: Run the Application

To start the application, run the following command:

```bash
docker run -it -p 8080:8080 api-hyperativa bash
./start.sh
```

The application will be available at [http://localhost:8080/](http://localhost:8080/).

### Running Tests

If you want to run tests, you can use `pytest` inside the bash terminal of the Docker container:

```bash
docker run -it api-hyperativa bash
pytest
```

## Summary of Commands

1. **Build Docker Image:**
   ```bash
   docker build -t api-hyperativa .
   ```

2. **Initialize the Database:**
   ```bash
   docker run -it api-hyperativa bash
   python manage.py db init
   python manage.py db migrate -m "Initial migration."
   python manage.py db upgrade
   ```

3. **Run the Application:**
   ```bash
   docker run -it -p 8080:8080 api-hyperativa bash
   ./start.sh
   ```

4. **Run Tests:**
   ```bash
   docker run -it api-hyperativa bash
   pytest
   ```

## Additional Information

- The application uses JWT for authentication.
- Endpoints are secured and require Bearer tokens.
- The API documentation is available via Swagger, integrated with Flask-RESTX.

Feel free to contribute or open issues for any problems you encounter.

---