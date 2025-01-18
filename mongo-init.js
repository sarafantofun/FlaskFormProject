// Switch to the specified database or create it if it doesn't exist
db = db.getSiblingDB("form_db");

// Insert sample form templates into the 'templates' collection
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
