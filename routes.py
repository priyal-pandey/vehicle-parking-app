from flask import render_template, redirect, url_for, request, flash, session
from app import app
from models import db,User
from werkzeug.security import generate_password_hash, check_password_hash

#decorator auth required


@app.route('/')
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template("user_dashboard.html")
    else:
        flash("Please login first","warning")
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash("Already logged in")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = User.query.filter_by(email = email).first()
            
            if user:
                if(check_password_hash(user.password, password)):
                    flash("Login successful","success")
                    session['user_id'] = user.user_id
                    return redirect(url_for('home'))
                else:
                    flash("Incorrect password. Please try again","error")
            else:
                flash("Account with this email does not exist. Try again or create account","error")
        else:
            flash("Please fill all fields","warning")

    return render_template("login.html")


@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if 'user_id' in session:
        flash("Already logged in")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        #validations
        if user:
            flash("An account with this email already exists","error")
        elif password1 != password2:
            flash("Passwords do not match","error")
        else:
            new_user = User(email = email, password = generate_password_hash(password1), name = name)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        
    return render_template("signup.html")

@app.route('/profile',methods=['GET','POST'])
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if request.method == 'POST':
            pass

        return render_template('profile.html', user = user)
    
    
    flash('Please login first')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        flash("You have been logged out", "success")
    else:
        flash("You are already logged out", "warning")
    
    return redirect(url_for('login'))
    


