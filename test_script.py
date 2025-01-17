import requests

# Base URL of the application to be tested
BASE_URL = "http://localhost:5000"

# List of test requests to validate the application
test_requests = [
    {"email": "test@example.com", "phone": "+7 123 456 78 90"},
    {"order_date": "2024-12-22", "user_name": "Ivan"},
    {"unknown_field": "random text", "phone": "+7 999 999 99 99"},
    {"unknown_email": "unknown@example.com", "unknown_phone": "+7 000 999 99 99"},
]


# Function to test the /get_form endpoint of the application
def test_get_form():
    """
    Send test requests to the /get_form endpoint and print the responses.
    This function simulates POST requests with different sets of form data to test
    the application's ability to match templates or classify data fields dynamically.
    """
    url = f"{BASE_URL}/get_form"
    for request_data in test_requests:
        response = requests.post(url, data=request_data)  # Sending form data as x-www-form-urlencoded
        print(f"Get Form Response: {response.status_code}, {response.json()}")  # Print the status and response body


if __name__ == "__main__":
    # Run the test for the /get_form endpoint
    test_get_form()
