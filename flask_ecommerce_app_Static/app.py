from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Rendering the HTML template

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
