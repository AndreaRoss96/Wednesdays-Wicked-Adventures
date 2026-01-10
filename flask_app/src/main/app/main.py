from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Booking, Park
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
    return render_template('profile.html', name=current_user.name)

@main.route('/bookings')
@login_required
def view_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.user_id).all()
    return render_template('bookings.html', bookings=bookings)

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
