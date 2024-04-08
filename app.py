import requests
from flask import Flask, render_template, request, url_for, redirect, flash, make_response
import pdfkit
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Initialize Flask app
app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = '1234567890'

# Initialize scheduler
scheduler = BackgroundScheduler()

# Set up email-related configurations
smtp_port = 587
smtp_server = "smtp.gmail.com"
email_from = "sender@gmail.com"  # Update with sender's email
passwd = "your secret password here"  # Update with sender's email password
subject = "Weather Report 📊 !!"

#A temporary list to hold data of email and city
last_sent_reports=[]

# Define routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/display-weather', methods=['POST'])
def display():
    city_or_zip = request.form.get('cityOrZip')
    email = request.form.get('email')
    x=[city_or_zip,email]
    last_sent_reports.append(x)
    print(last_sent_reports)
    if city_or_zip == "" or email == "":
        return redirect(url_for('index'))

    # Fetch weather data
    api_key = 'your_secret_api_key'  # Replace with your API key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_or_zip}'
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        flash('Error: {}'.format(data['error']['message']))
        return redirect(url_for('index'))
    else:
        return render_template('weather.html', data=data)


@app.route('/generate_report', methods=['POST'])
def generate_report():
    credentials = request.form.get('last')
    data_string = credentials.strip('[]')
    elements = data_string.split(", ")

    text = [element.strip("'") for element in elements]
    city_or_zip=text[0]

    # Fetch weather data
    api_key = 'your_secret_api_key'  # Replace with your API key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_or_zip}'
    response = requests.get(url)
    data = response.json()

    # Render the weather template to HTML with the provided data
    rendered_html = render_template('weather.html', data=data)

    # Generate PDF from the rendered HTML
    pdf = pdfkit.from_string(rendered_html, False)

    # Create response with PDF as attachment
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=weather_report.pdf'

    return response


@app.route('/send_email', methods=['POST'])
def send_email():
    credentials = request.form.get('last')
    data_string = credentials.strip('[]')
    elements = data_string.split(", ")
    city_or_zip = elements[0]
    email_to_stringformat = elements[1]
    email_to = [email_to_stringformat]

    # Fetch weather data
    api_key = 'your_secret_api_key'  # Replace with your API key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_or_zip}'
    response = requests.get(url)
    data = response.json()

    # Render the weather template to HTML with the provided data
    rendered_html = render_template('weather.html', data=data)

    # Generate PDF from the rendered HTML
    pdf = pdfkit.from_string(rendered_html, False)

    # Send emails
    for person in email_to:
        # Construct email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject
        body = "Please find attached the weather report."
        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(pdf)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f"attachment; filename=weather_report.pdf")
        msg.attach(attachment)
        text = msg.as_string()

        # Connect to SMTP server and send email
        print("Connecting to server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_from, passwd)
            print("Succesfully connected to server")
            print()
            print(f"Sending email to: {person}...")
            server.sendmail(email_from, person, text)
            print(f"Email sent to: {person}")
            print()

    server.quit()

    success_message = "Email sent successfully"
    redirect_url = url_for('index')  # Assuming your index route is named 'index'
    return f"{success_message}. Redirecting back to home in 5 seconds...<meta http-equiv='refresh' content='5;URL={redirect_url}'>"


@app.route('/scheduling', methods=['POST'])
def scheduling():
    # Schedule email sending job
    scheduler.add_job(scheduled_mails, 'interval', minutes=15)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    
    success_message = "Email scheduled successfully You will get mail every 15 min"
    redirect_url = url_for('index')  # Assuming your index route is named 'index'
    
    return f"{success_message}. Redirecting back to home in 5 seconds...<meta http-equiv='refresh' content='5;URL={redirect_url}'>"


# Define scheduled task
def scheduled_mails():
    with app.app_context():
        for credentials in last_sent_reports:
            city_or_zip = credentials[0]
            email_to_stringformat = credentials[1]

            # Fetch weather data
            api_key = 'your_secret_api_key'  # Replace with your API key
            url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_or_zip}'
            response = requests.get(url)
            data = response.json()

            # Render the weather template to HTML with the provided data
            with app.test_request_context():
                rendered_html = render_template('weather.html', data=data)

            # Generate PDF from the rendered HTML
            pdf = pdfkit.from_string(rendered_html, False)

            # Send email to each recipient
            # Construct email
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = email_to_stringformat
            msg['Subject'] = subject
            body = "Please find attached the weather report."
            msg.attach(MIMEText(body, 'plain'))

            # Attach PDF
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(pdf)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f"attachment; filename=weather_report.pdf")
            msg.attach(attachment)
            text = msg.as_string()

            
            # Connect to SMTP server and send email
            print("Connecting to server...")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_from, passwd)
                print("Succesfully connected to server")
                print()
                print(f"Sending email to: {email_to_stringformat}...")
                server.sendmail(email_from, email_to_stringformat, text)
                print(f"Email sent to: {email_to_stringformat}")
                print()

        server.quit()


# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
