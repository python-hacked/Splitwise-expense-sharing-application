# Splitwise-expense-sharing-application

This is a simple Django web application for splitting expenses among users. Users can add their expenses, view balances, and send email notifications for pending payments.

## Prerequisites

Make sure you have the following installed on your system:

- Python
- Django

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/expense-splitting-app.git

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


# Expense Splitting Application

This is a Django web application for managing expenses and splitting bills among friends or participants.

## Features

- **Add Users**: Easily add participants to the application.

- **Add Expenses**: Record expenses and split bills among participants.

- **View Balances**: View balances for each participant to keep track of who owes whom.

- **Send Notifications**: Send notifications to participants for pending amounts.

## Getting Started

1. Clone this repository to your local machine:


2. Navigate to the project directory:


7. Access the application in your web browser at [http://localhost:8000/](http://localhost:8000/).

## Usage

- To add users, navigate to the "Add User" section.

- To add expenses, go to the "Add Expense" section and record expenses, specifying the payer and participants.

- View balances in the "View Balances" section.

- Send notifications for pending amounts in the "Send Notifications" section.


## Navigation URLs

- `/` (Home): This is the landing page of the application.
- `/ragister/` (Add User): Use this page to add a new user.
- `/add_expense/` (Add Expense): Add a new expense, specifying the payer and participants.
- `/view_balances/` (View Balances): View the balances of all participants.
- `/split_equally/` (Split Equally): Split an expense equally among selected participants.
- `/split_equally/success/` (Split Equally Success): A confirmation page after splitting equally.
- `/split_exact/` (Split Exact): Split an expense with custom amounts specified for participants.
- `/send_email/` (Send Email): Send a notification email regarding an expense.

## API URLs

- `/api/add_expense/` (Add Expense API): API endpoint to add an expense.
- `/api/view_balances/` (View Balances API): API endpoint to view balances of participants.
- `/api/send_notification/` (Send Notification API): API endpoint to send notification emails.


api.py (inside the 'api' folder):

AddExpenseView is an API view to add an expense. It accepts a POST request with a JSON payload that includes 'description,' 'amount,' and 'participants.'
It creates a new expense and calculates the shares for each participant, updating the balances accordingly.
If the request is successful, it returns a JSON response with {"success": True} and a status code of 201 (Created).
In case of an error, it returns a JSON response with an error message and a status code of 500 (Internal Server Error).
serializers.py (inside the 'api' folder):

This file defines the serializer for sending notifications.
It expects a JSON payload with 'email' and 'amount.'
The serializer is used to validate the data received in a notification request.
If the data is valid, it proceeds to send an email notification.

Adding an Expense:

Endpoint: /api/add_expense/
HTTP Method: POST
Request Payload:
description (string): A brief description of the expense.
amount (decimal): The total expense amount.
participants (array of strings): An array of participant names who are sharing the expense.

## Also i use url in insode of url.py file use for this url as API
 ## API URLs

- `/api/add_expense/` (Add Expense API): API endpoint to add an expense.
- `/api/view_balances/` (View Balances API): API endpoint to view balances of participants.
- `/api/send_notification/` (Send Notification API): API endpoint to send notification emails.

Example Request JSON:
{
  "description": "Groceries",
  "amount": 100.00,
  "participants": ["Alice", "Bob", "Charlie"]
}

Sending a Notification:

Endpoint: /api/send_notification/
HTTP Method: POST
Request Payload:
email (string): The recipient's email address to send the notification.
amount (decimal): The amount to be included in the notification.

Example Request JSON:
{
  "email": "recipient@example.com",
  "amount": 25.00
}

