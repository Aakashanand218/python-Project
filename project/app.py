from flask import Flask, request, redirect, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main form page."""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <h2>Error</h2>
        <p>Template error: {e}</p>
        <p>Ensure 'index.html' exists in the 'templates' folder.</p>
        <a href="/">Try Again</a>
        """

@app.route('/save', methods=['POST'])
def save_data():
    """Handle form submission and save data to a file."""
    name = request.form.get('name')
    age = request.form.get('age')

    # Validate inputs
    if not name or not age:
        return """
        <h2>Error</h2>
        <p>Invalid Input: Both Name and Age are required.</p>
        <a href="/">Go Back</a>
        """
    
    try:
        age = int(age)
        if age < 0 or age > 120:
            return """
            <h2>Error</h2>
            <p>Invalid Input: Age must be between 0 and 120.</p>
            <a href="/">Go Back</a>
            """
        if len(name.strip()) == 0 or len(name) > 100:
            return """
            <h2>Error</h2>
            <p>Invalid Input: Name must be between 1 and 100 characters.</p>
            <a href="/">Go Back</a>
            """
    except (ValueError, TypeError):
        return """
        <h2>Error</h2>
        <p>Invalid Input: Age must be a valid number.</p>
        <a href="/">Go Back</a>
        """

    # Save to file
    try:
        file_path = 'D:/Btech/Coding/Btech Python/project/user_data.txt'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'a') as file:
            file.write(f"Name: {name}, Age: {age}\n")
        return """
        <h2>Success</h2>
        <p>Data saved successfully!</p>
        <a href="/">Go Back</a>
        """
    except (IOError, PermissionError) as e:
        return f"""
        <h2>Error</h2>
        <p>File error: {e}</p>
        <a href="/">Go Back</a>
        """

if __name__ == '__main__':
    app.run(debug=True)