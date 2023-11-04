# FastAPISecureQR

This is a FastAPI application that provides endpoints for user authentication and QR code check-in management.

## Features

- User authentication (sign up and login)
- QR code check-in and check-out
- Middleware for user authentication
- Cross-Origin Resource Sharing (CORS) support for client-side interaction

## Tech Stack

- FastAPI
- PyMongo for MongoDB interaction
- Pydantic for data validation
- Python-JOSE for JWT token generation
- Bcrypt for password hashing

## Installation

Ensure you have Python 3.7+ installed on your system before starting the installation.
- Clone the repository
   ```bash
        git clone https://github.com/sarparslan/FastAPISecureQR.git
  ```
 - Navigate to the project directory

   ```bash
        cd FastAPISecureQR
      ```
 - Install the dependencies

   ```bash
        pip install -r requirements.txt
    ```
 - To start the FastAPI server, run the following command

   ```bash
        uvicorn main:app --reload
    ``` 

The API will be available at http://127.0.0.1:8000.

  ## API Endpoints
  -> Authentication
  - POST /auth/create_user/: Create a new user. 
  - POST /auth/login: Authenticate a user and return a JWT.
  
  -> User Actions
  - POST /user/addQr: Add a QR code check-in for the authenticated user.
  - PUT /user/update_end_time: Update the check-out time for a QR code.

  ```env
      MONGODB_URI=<your_mongodb_connection_string>
      JWT_SECRET_KEY=<your_jwt_secret_key>
      JWT_ALGORITHM=HS256 # Or your preferred algorithm
 ```
Configuration
In the DB/db.py file, make sure to update the uri variable with your MongoDB connection string.
  
