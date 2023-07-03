# Mass Mail App

This is a Django Rest Framework (DRF) application that allows users to send emails using Celery as a task queue and Anymail with Mailgun as the email service provider. The application provides a simple and efficient way to send emails asynchronously.

## Features

- User registration and authentication using Simple JWT
- Sending emails asynchronously using Celery and Anymail with Mailgun
- RESTful API endpoints for sending emails

## Requirements

Make sure you have the following dependencies installed:

- Python 3.8+
- Redis (as Celery message broker)
- Anymail
- Mailgun

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/JoseMiracle/Mass_e-mail_app.git
   ```

2. Change to the project directory:

   ```
   cd Mass_e-mail_app
   ```

3. Create and activate a virtual environment:

   ```
   python3 -m venv venv
   For Linux: source venv/bin/activate
   For Windows: venv\Scripts\activate 
   ```

4. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

5. Start a Redis server. Make sure it is running and accessible.

6. Apply migrations to set up the database:

   ```
   python manage.py migrate
   ```

7. Start the Celery worker to handle email sending tasks:

   ```
   celery -A send_mail_app worker --loglevel=info
   ```

8. Run the Django development server:

   ```
   python manage.py runserver
   ```

9. Access the application at `http://localhost:8000`.

## Authentication

Authentication in this application is based on JSON Web Tokens (JWT). To access protected endpoints, include the JWT token in the `Authorization` header as follows:

```http
Authorization: Bearer <jwt-token>
```
## Configuration

1. Create environment variable file `.env` and update the necessary configurations.

   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost

   # Redis configurations
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0

   
   # Anymail with Mailgun configurations
   EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   ANYMAIL_MAILGUN_API_KEY=your_mailgun_api_key
   ANYMAIL_MAILGUN_SENDER_DOMAIN=your_mailgun_sender_domain
   ```

2. Update the email configuration in `settings.py` file etc.

   ```python
   EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
   ANYMAIL = {
       "MAILGUN_API_KEY": "your_mailgun_api_key",
       "MAILGUN_SENDER_DOMAIN": "your_mailgun_sender_domain",
   }
   DEFAULT_FROM_EMAIL = 'your_email@example.com'
   ```

## API Endpoints

The Send Mail App provides the following API endpoints:

- **POST** `api/users/sign-up/` - This is for signing up
- **POST** `api/users/sign-in/` - This is for signing in, and access-token will be generated for authentication used in other endpoint
- **PATCH** `api/users/change-password/` - This is for changing a user's password requires authentication
- **PUT**  `api/users/update-profile/` - This is for upadting user's profile, requires authentication
- **POST** `api/users/otp-generation/` - This is used in generating otp for reseting password
- **POST** `api/users/otp-verification/`- This is for verifying the OTP the user supplies
- **POST** `api/users/reset-password/` - This for resetting users password
- **POST** `api/mails/send-mails/` - This for sending mails
- **POST** `api/mails/get-sent-mails/` - This is for retrieving the info of people mails were sent to



## API Documentation

The API documentation is automatically generated using DRF Spectacular and presented using Swagger UI. You can access the interactive API documentation by visiting `http://localhost:8000/api/schema/swagger-ui/#/`. It provides a user-friendly interface to explore the available endpoints, view request/response formats, and test the API directly from the browser. The documentation includes detailed descriptions of the API endpoints, request/response schemas, and authentication requirements.

To inform your viewers that more functionalities will be added to the Send Mail App in the future, you can include a section in your README file or create a separate section on your project's documentation or website. Here's an example of how you can communicate this information:

## Future Enhancements

We are continuously working to enhance the functionality and features of the Mass Mail App. Here are some of the planned additions and improvements that will be implemented in future updates:

- Support for email attachments: We will add the ability to attach files to the emails being sent, allowing users to include important documents or media files.

- Email templates: We plan to introduce pre-defined email templates that users can utilize, making it easier to compose and send commonly used emails with minimal effort.

- Email scheduling: We aim to incorporate a scheduling feature that enables users to specify a future date and time for their emails to be sent automatically.

- Additional authentication methods: Currently, the app supports authentication using Simple JWT. In the future, we plan to add support for other authentication methods such as OAuth or social logins.

- Improved error handling and logging: We will enhance the error handling and logging mechanisms to provide more informative error messages and better visibility into the system's behavior.

- UI enhancements: While the app currently provides a RESTful API, we are working on developing a user-friendly web interface that will offer a seamless and intuitive experience for managing email sending tasks.

We appreciate your feedback and suggestions as we continue to evolve the Mass Mail App. Stay tuned for updates as we strive to make the app more powerful and feature-rich.
