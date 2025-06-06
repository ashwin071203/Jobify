from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure database
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_tracker.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Change this in production

db = SQLAlchemy(app)

# Database Models
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    education = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def dashboard():
    resume_count = Resume.query.count()
    job_count = JobApplication.query.count()
    recent_jobs = JobApplication.query.order_by(JobApplication.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', 
                         resume_count=resume_count,
                         job_count=job_count,
                         recent_jobs=recent_jobs)

@app.route('/resumes')
def resume_list():
    resumes = Resume.query.order_by(Resume.created_at.desc()).all()
    return render_template('resumes.html', resumes=resumes)

@app.route('/resumes/create', methods=['GET', 'POST'])
def create_resume():
    if request.method == 'POST':
        data = request.form
        resume = Resume(
            name=data['name'],
            email=data['email'],
            education=data['education'],
            skills=data['skills'],
            experience=data['experience']
        )
        db.session.add(resume)
        db.session.commit()
        return redirect(url_for('resume_list'))
    return render_template('resume_form.html')

@app.route('/resumes/<int:id>/edit', methods=['GET', 'POST'])
def edit_resume(id):
    resume = Resume.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        resume.name = data['name']
        resume.email = data['email']
        resume.education = data['education']
        resume.skills = data['skills']
        resume.experience = data['experience']
        db.session.commit()
        return redirect(url_for('resume_list'))
    return render_template('resume_form.html', resume=resume)

@app.route('/resumes/<int:id>/delete', methods=['POST'])
def delete_resume(id):
    resume = Resume.query.get_or_404(id)
    db.session.delete(resume)
    db.session.commit()
    return redirect(url_for('resume_list'))

@app.route('/jobs')
def job_list():
    jobs = JobApplication.query.order_by(JobApplication.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        data = request.form
        job = JobApplication(
            company=data['company'],
            role=data['role'],
            application_date=datetime.strptime(data['application_date'], '%Y-%m-%d'),
            status=data['status'],
            notes=data['notes']
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('job_list'))
    return render_template('job_form.html')

@app.route('/jobs/<int:id>/edit', methods=['GET', 'POST'])
def edit_job(id):
    job = JobApplication.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        job.company = data['company']
        job.role = data['role']
        job.application_date = datetime.strptime(data['application_date'], '%Y-%m-%d')
        job.status = data['status']
        job.notes = data['notes']
        db.session.commit()
        return redirect(url_for('job_list'))
    return render_template('job_form.html', job=job)

@app.route('/jobs/<int:id>/delete', methods=['POST'])
def delete_job(id):
    job = JobApplication.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('job_list'))

# API Endpoints
@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    resumes = Resume.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'email': r.email,
        'education': r.education,
        'skills': r.skills,
        'experience': r.experience,
        'created_at': r.created_at.isoformat()
    } for r in resumes])

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = JobApplication.query.all()
    return jsonify([{
        'id': j.id,
        'company': j.company,
        'role': j.role,
        'application_date': j.application_date.isoformat(),
        'status': j.status,
        'notes': j.notes,
        'created_at': j.created_at.isoformat()
    } for j in jobs])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('FLASK_ENV') == 'development') 