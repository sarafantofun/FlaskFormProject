import os
import re
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# MongoDB configuration from environment variables
MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Connect to MongoDB
client = MongoClient(
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource=admin"
)
db = client[MONGO_DB_NAME]
templates_collection = db["templates"]


def detect_field_type(value):
    """
    Detect the type of a given field based on its value.
    The detection order is as follows: date, phone, email, and text.
    Args:
        value (str): The value to analyze.
    Returns:
        str: The type of the field ("date", "phone", "email", or "text").
    """
    # Check for date in the format YYYY-MM-DD
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return "date"
    except ValueError:
        pass

    # Check for date in the format DD.MM.YYYY
    try:
        datetime.strptime(value, "%d.%m.%Y")
        return "date"
    except ValueError:
        pass

    # Check for phone number in the format +7 XXX XXX XX XX
    if re.fullmatch(r"\+7 \d{3} \d{3} \d{2} \d{2}", value):
        return "phone"

    # Check for a valid email address
    if "@" in value and "." in value.split("@")[-1]:
        return "email"

    # Default to text if no other type matches
    return "text"


@app.route("/get_form", methods=["POST"])
def get_form():
    """
    Identify the most suitable form template for the given input data.
    The function compares incoming data with stored form templates
    to find the best match based on field names and types.
    Returns:
        JSON response:
            - If a matching template is found: {"template_name": "template_name"}.
            - If no match is found: {"field_name": "FIELD_TYPE"} for each field.
    """
    try:
        # Parse input data from the POST request
        data = request.form.to_dict()

        # Retrieve all templates from the database
        templates = list(templates_collection.find())
        best_match = None
        max_matched_fields = 0

        for template in templates:
            template_name = template.pop("name")  # Extract the template name
            template.pop("_id", None)  # Remove MongoDB's internal _id field

            # Count matching fields by name and type
            matched_fields = sum(
                1
                for field, field_type in template.items()
                if field in data and detect_field_type(data[field]) == field_type
            )

            # Update the best match if this template has more matching fields
            if matched_fields > max_matched_fields:
                best_match = template_name
                max_matched_fields = matched_fields

        # Return the best matching template, if found
        if best_match:
            return jsonify({"template_name": best_match}), 200

        # If no matching template, detect field types on the fly
        field_types = {key: detect_field_type(value) for key, value in data.items()}
        return jsonify(field_types), 404

    except Exception as e:
        # Handle errors and return a meaningful error message
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    """
    Run the Flask application.
    The application listens on all interfaces at port 5000.
    """
    app.run(host="0.0.0.0", port=5000)
