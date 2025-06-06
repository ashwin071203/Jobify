# Resume & Job Tracker

A simple and efficient web application for managing resumes and job applications. Built with Flask and TailwindCSS.

## Features

- User Dashboard with key statistics
- Resume Manager (Create, Edit, Delete)
- Job Application Tracker with filtering and search
- Mobile-responsive design
- SQLite database for data storage

## Tech Stack

- Backend: Python (Flask)
- Frontend: HTML, TailwindCSS, JavaScript
- Database: SQLite
- Template Engine: Jinja2

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

2. Run the development server:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Deployment

### Deploying to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Add the following environment variables:
   - `FLASK_ENV=production`
   - `FLASK_APP=app.py`

### Deploying to Heroku

1. Create a new Heroku app
2. Add the Python buildpack:
```bash
heroku buildpacks:set heroku/python
```

3. Deploy the application:
```bash
git push heroku main
```

## Project Structure

```
resume-tracker/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── resumes.html
│   ├── resume_form.html
│   ├── jobs.html
│   └── job_form.html
└── static/            # Static files (CSS, JS)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 