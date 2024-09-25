# Shift Scheduling System

#### Video Demo: [<URL HERE>](https://www.youtube.com/watch?v=mmR2QYuOBvw)

#### Description:
This project is a Shift Scheduling System that automates the creation and distribution of work schedules for a team. It reads team member information from a CSV file, generates a 30-day schedule, creates a PDF of the schedule, and emails it to each team member.
The whole process of this project involved chosing nad discarding packages to make this script.
FPDF was initially chosen for the pdf generation but i had to discard it after research beacuse the whole process involved alot of code written on my part, unlike using ReportLab .
You must Setup the correct env enironment variables 
copy .env.examples into .env and set it up

### Key Functions:

1. `is_csv_file(filename: str) -> bool`:
   - First method ensures file format is correct  
   - Checks if the provided filename has a .csv extension.

2. `read_individuals_from_csv(filename)`:
   - Reads the CSV file containing team member information.
   - Returns a list of dictionaries, where each dictionary represents an individual with their details.

3. `create_shift_schedule(individuals: list, num_days: int = 30)`:
   - Generates a fair shift schedule for the specified number of days (default 30).
   - Assigns individuals to three shifts: "12 AM - 8 AM", "8 AM - 4 PM", "4 PM - 12 AM".
   - Ensures even distribution of shifts among team members.
   - Returns a dictionary with dates as keys and shift assignments as values.

4. `generate_pdf(schedule: dict, filename: str)`:
   - Creates a PDF document of the shift schedule using ReportLab.
   - I really considered usind fpdf library here but choose Report Lab Less code written
   - Organizes the schedule into a table format, grouped by weeks.
   - Includes each person's name, phone number, and email in their assigned shifts.

5. `send_email(recipient_info: dict, subject: str, body: str, attachment: str) -> bool`:
   - Sends an email with the PDF schedule attached to each team member.
   - Uses SMTP details from environment variables for secure email configuration.
   - Returns True if the email was sent successfully, False otherwise.

6. `main()`:
   - Orchestrates the entire process:
     1. Validates command-line arguments
     2. Reads the CSV file
     3. Generates the schedule
     4. Creates the PDF
     5. Emails the schedule to each team member

### Usage:
1. Prepare a CSV file with team member information (firstname, lastname, email, phone).
2. Run cp .env.example .env to copy environment variable of the smtp server (SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)
3. Run pip install -r requirements.txt to install all packages used
3. Run the script:
   ```
   python project.py names.csv
   ```

This script streamlines the shift scheduling process and gives a fair distribution of shifts and efficient communication with team members.