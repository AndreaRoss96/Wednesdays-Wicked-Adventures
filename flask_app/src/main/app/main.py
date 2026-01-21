from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Booking, Park, Message
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    parks = Park.query.all()
    return render_template('index.html', parks=parks)

@main.route('/parks/<int:park_id>')
def park_detail(park_id):
    park = Park.query.get_or_404(park_id)
    return render_template('park_detail.html', park=park)

@main.route('/profile')
@login_required
def profile():
    if current_user.has_role('admin'):
        return redirect(url_for('admin.index'))
    return render_template('profile.html', name=current_user.name)

@main.route('/booking/new')
@login_required
def new_booking():
    parks = Park.query.all()
    return render_template('new_booking.html', parks=parks)

@main.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'POST':
        booking = Booking(
            user_id=current_user.user_id,
            park_id=request.form['park_id'],
            date=datetime.fromisoformat(request.form['date']),
            num_tickets=int(request.form['num_tickets']),
            health_safety='health_safety' in request.form
        )

        db.session.add(booking)
        db.session.commit()

        return redirect(url_for('main.profile'))

    parks = Park.query.all()
    return redirect(url_for('main.profile'))

@main.route('/health-safety-guidelines')
@login_required
def health_safety_guidelines():
    current_date = datetime.now()
    return render_template('health_safety_guidelines.html', now=current_date)

@main.route('/contact', methods=['GET','POST'])
def contact():
   
    try:
        referrer = request.referrer or url_for('main.index')
        
        if '#contact' in referrer:
            referrer = referrer.split('#')[0]
        
        if not all([request.form.get('name'), 
                    request.form.get('email'), 
                    request.form.get('message')]):
            flash('Please fill in all fields.', 'error')
            return redirect(referrer + '#contact')
        
        message = Message(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        
    except Exception as e:
        print(f"Error sending message: {e}")
        flash('Sorry, there was an error sending your message. Please try again.', 'error')
    
    return redirect(referrer + '#contact')