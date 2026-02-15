from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User
from forms import RegisterForm, LoginForm
from config import Config

from forms import JobForm
from models import Job
from models import Application


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

def is_admin():
    return current_user.is_authenticated and current_user.email == 'admin@jobportal.com'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')




@app.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'employer':
        flash('Access denied. Employers only.', 'danger')
        return redirect(url_for('dashboard'))

    form = JobForm()

    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            salary=form.salary.data,
            description=form.description.data,
            posted_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()

        flash('Job posted successfully!', 'success')
        return redirect(url_for('my_jobs'))

    return render_template('post_job.html', form=form)

@app.route('/my-jobs')
@login_required
def my_jobs():
    if current_user.role != 'employer':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))

    jobs = Job.query.filter_by(posted_by=current_user.id).all()
    return render_template('my_jobs.html', jobs=jobs)

@app.route('/jobs')
def jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/apply/<int:job_id>')
@login_required
def apply_job(job_id):
    if current_user.role != 'jobseeker':
        flash('Only job seekers can apply for jobs.', 'danger')
        return redirect(url_for('job_detail', job_id=job_id))

    existing_application = Application.query.filter_by(
        job_id=job_id,
        user_id=current_user.id
    ).first()

    if existing_application:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('job_detail', job_id=job_id))

    application = Application(
        job_id=job_id,
        user_id=current_user.id
    )
    db.session.add(application)
    db.session.commit()

    flash('Application submitted successfully!', 'success')
    return redirect(url_for('jobs'))

@app.route('/my-applications')
@login_required
def my_applications():
    if current_user.role != 'jobseeker':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))

    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('my_applications.html', applications=applications)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not is_admin():
        flash('Admin access only.', 'danger')
        return redirect(url_for('dashboard'))

    users = User.query.all()
    jobs = Job.query.all()

    return render_template('admin_dashboard.html', users=users, jobs=jobs)

@app.route('/admin/delete-job/<int:job_id>')
@login_required
def delete_job_admin(job_id):
    if not is_admin():
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard'))

    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()

    flash('Job deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))









@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

