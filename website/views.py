from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    city = None
    month = None
    year = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        month = request.form.get('month')
        year = request.form.get('year')
        
        if not city:
            flash('City is required!', category='error')
        if not month:
            flash('Month is required!', category='error')
        if not year:
            flash('Year is required!', category='error')
            
    return render_template('home.html', city=city, month=month, year=year)
