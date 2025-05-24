# Dock Inn Queue Management System

A web-based queue management system built with Django that helps manage and track customer queues in various service areas.

## Features

- Queue Management System
- User Authentication and Authorization
- Dashboard for Queue Monitoring
- QR Code Generation
- PDF Generation for Queue Tickets
- Multiple Queue Support

## Project Structure

- `accounts/`: User authentication and authorization
- `dashboards/`: Queue monitoring and analytics
- `queues/`: Core queue management functionality
- `static/`: Static files (CSS, JavaScript, images)
- `templates/`: HTML templates

## Requirements

- Python 3.x
- Django 4.2.1
- PostgreSQL (via psycopg2-binary)
- Additional dependencies listed in [requirements.txt](requirements.txt)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the application at `http://localhost:8000`
2. Log in with your credentials
3. Use the dashboard to monitor queues
4. Manage queue entries through the queue management interface

## Development

The project uses Django's built-in development server for local development. Make sure to set up your environment variables and database configuration before running the application.

## Security

- The application uses Django's built-in security features
- CSRF protection is enabled
- Session management is implemented
- User authentication is required for most features

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

