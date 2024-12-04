import requests
import time
import logging
import random
import string
import smtplib
import os
from email.mime.text import MIMEText

# Setup logging
logging.basicConfig(filename='monitoring.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Environment Variables for Configurations
MONITOR_INTERVAL = int(os.getenv('MONITOR_INTERVAL', '600'))  # Default to 10 minutes
ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', '3'))  # Number of consecutive failures to trigger alert

# Email Configuration for Alerting
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'your_email@example.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your_password')
ALERT_EMAIL_TO = os.getenv('ALERT_EMAIL_TO', 'alert_receiver@example.com')

# URLs to monitor
urls = {
    "Word Count": "http://editor-proxy-router:80/api/wordcount/?text=",
    "Character Count": "http://editor-proxy-router:80/api/charcount/?text=",
    "Average Word Length": "http://editor-proxy-router:80/api/avgWordLength/?text=",
    "Count Vowels": "http://editor-proxy-router:80/api/countVowels/?text=",
    "Count Commas": "http://editor-proxy-router:80/api/countCommas/?text=",
    "Count Palindromes": "http://editor-proxy-router:80/api/countPalindromes/?text="
}

# Thresholds for performance
timeout_threshold = 5  # seconds

failure_counts = {name: 0 for name in urls.keys()}

# Function to generate random text
def generate_random_text():
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(5, 20)))

# Function to send alert email
def send_alert(service_name, error_message):
    subject = f"Alert: Service Failure Detected for {service_name}"
    body = f"Service {service_name} has failed.\n\nError Details:\n{error_message}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = ALERT_EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, [ALERT_EMAIL_TO], msg.as_string())
        server.quit()
        logging.info(f"Alert sent for {service_name}")
    except Exception as e:
        logging.error(f"Failed to send alert email: {str(e)}")

# Function to monitor services
def monitor_services():
    while True:
        for name, base_url in urls.items():
            random_text = generate_random_text()
            url = f"{base_url}{random_text}"
            try:
                # Debug print statement
                print(f"Checking {name} at URL: {url}")
                
                # Start time to measure response time
                start_time = time.time()
                
                # Request to service URL with timeout
                response = requests.get(url, timeout=timeout_threshold)
                
                # End time after receiving response
                end_time = time.time()
                
                # Calculating response time
                response_time = end_time - start_time

                # Check if response was successful
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data and data["error"] is False:
                        expected_count = len(random_text.split())
                        if name == "Word Count" and data["answer"] != expected_count:
                            logging.error(f"{name}: ERROR - Incorrect word count. Expected {expected_count}, got {data['answer']}")
                            failure_counts[name] += 1
                        else:
                            logging.info(f"{name}: SUCCESS - Response Time: {response_time:.2f}s - Data: {data}")
                            failure_counts[name] = 0
                    else:
                        logging.error(f"{name}: ERROR - Unexpected Response Data: {data}")
                        failure_counts[name] += 1
                else:
                    logging.error(f"{name}: ERROR - Status Code: {response.status_code}")
                    failure_counts[name] += 1

            # Handle request timeout exception
            except requests.exceptions.Timeout:
                logging.error(f"{name}: ERROR - Request Timed Out after {timeout_threshold} seconds")
                failure_counts[name] += 1

            # Handle any other exceptions
            except Exception as e:
                logging.error(f"{name}: ERROR - Exception occurred: {str(e)}")
                failure_counts[name] += 1

            # Send alert if failure count exceeds threshold
            if failure_counts[name] >= ALERT_THRESHOLD:
                send_alert(name, f"{failure_counts[name]} consecutive failures.")

        # Debug print statement to indicate end of the monitoring cycle
        print("Waiting before next monitoring cycle...")
        
        # Wait for the configured interval before running the checks again
        time.sleep(MONITOR_INTERVAL)

# Entry point of the script
if __name__ == "__main__":
    monitor_services()
