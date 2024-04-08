# Weather Report App

## Overview
Weather Report App is a Flask-based web application that fetches weather data from an external API, generates weather reports in PDF format, and sends them via email. It also provides scheduling functionality to automate email sending at regular intervals.

## Dependencies
- Python 3.x
- Flask
- Requests
- APScheduler
- pdfkit
- smtplib (standard library)
- email (standard library)

## Setup
1. Install Python 3.x.
2. Install required dependencies using `pip install flask requests apscheduler pdfkit`.

## Configuration
1. Replace `'your_secret_api_key'` in the code with your actual API key obtained from a weather service provider.
2. Update `email_from` with your email address.
3. Update `passwd` with your email password.
4. Ensure your email provider allows SMTP access and uses the correct SMTP server and port.

## Usage
1. Run the Flask application by executing the script.
2. Access the application through a web browser.
3. Enter a city name or ZIP code and an email address to receive weather reports.
4. Choose to either view the weather report on the web page, generate a PDF report, or send the report via email.
5. Optionally, schedule automatic email sending at regular intervals.

## Routes
- `/`: Homepage route. Displays a form to input city/ZIP and email.
- `/display-weather`: POST route to fetch weather data and display it on the web page.
- `/generate_report`: POST route to generate a PDF report and download it.
- `/send_email`: POST route to send the weather report via email.
- `/scheduling`: POST route to schedule automatic email sending.

## Functions
- `index()`: Renders the index.html template for the homepage.
- `display()`: Fetches weather data from the API and displays it on the web page.
- `generate_report()`: Generates a PDF report of the weather data.
- `send_email()`: Sends the weather report via email to the provided address.
- `scheduling()`: Schedules automatic email sending at regular intervals.
- `scheduled_mails()`: Sends scheduled emails with weather reports.

## Notes
- Ensure proper error handling and validation for user inputs and API responses.
- Securely store and manage sensitive information such as API keys and email passwords.
- Test the application thoroughly before deploying it to production.
