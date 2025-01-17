# FlaskFormProject

This application provides a web service to detect forms based on input field names and their types. It uses Flask for the web server and MongoDB to store form templates.

---

## Features
- Detects the most suitable form template for given input fields.
- Supports on-the-fly field type detection when no template matches.
- Four field types are validated:
  - `email`
  - `phone` (format: `+7 xxx xxx xx xx`)
  - `date` (formats: `YYYY-MM-DD` or `DD.MM.YYYY`)
  - `text`
- API endpoints for testing and template detection.

---

## Requirements

- **Python**: >= 3.11
- **MongoDB**: Configured with Docker
- **Dependencies**: Managed via Poetry

---

## Installation

### 1. Clone the Repository
```bash
$ git clone https://github.com/sarafantofun/FlaskFormProject.git
$ cd FlaskFormProject
```

### 2. Set Up Environment Variables
Create a `.env` file with the following contents:
```env
FLASK_APP=main.py
FLASK_ENV=development
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB_NAME=form_db
SECRET_KEY=your_secret_key_here
```

### 3. Build and Start Docker Containers
Ensure Docker and Docker Compose are installed. Then run:
```bash
$ docker-compose up --build
```
This will start the Flask application and MongoDB in separate containers.

---

## Usage

### 1. Add Form Templates
Form templates are preloaded into MongoDB from the `mongo-init.js` file. Example:
```javascript
db = db.getSiblingDB("form_db");
db.templates.insertMany([
    {
        name: "Contact Form",
        email: "email",
        phone: "phone"
    },
    {
        name: "Order Form",
        order_date: "date",
        user_name: "text",
        user_email: "email"
    }
]);
```

### 2. API Endpoints
#### **POST /get_form**
Detects the form template matching the input fields.

**Example Request**:
```bash
$ curl -X POST http://localhost:5000/get_form \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "email=test@example.com&phone=%2B7%20123%20456%2078%2090"
```
**Response**:
```json
{
    "template_name": "Contact Form"
}
```

If no matching template is found:
```json
{
    "email": "email",
    "phone": "phone"
}
```

---

### **Testing the Application**

The application includes a test script `test_script.py` located within the Docker container. This script sends predefined test requests to the `/get_form` endpoint to verify template matching functionality.

#### **How to Run Tests**

1. **Start the application**: Make sure the application is running inside its container. Use:
   ```bash
   docker-compose up
   ```
2. **Access the container**:
   ```bash
   docker exec -it flask_form bash
   ```
3. **Run the test script** inside the container:
   ```bash
   python test_script.py
   ```

The script will output the results of the test requests, including the status code and response data for each case.

---

## Deployment

1. Set `FLASK_ENV` to `production` in the `.env` file.
2. Rebuild and restart the Docker containers:
```bash
$ docker-compose up --build
```

---

## License
This project is licensed under the MIT License.

---

## Author
For questions or feedback, please reach out to Tanya Sarafanova.
