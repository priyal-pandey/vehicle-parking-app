from flask import render_template, redirect, url_for, request, flash, session
from app import app
from models import db,User,Lot,Spot, Reserve, Payment
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

#decorator for checking if user is logged in
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash("Please login first","warning")
            return redirect(url_for('login'))
    return inner

#decorator for checking if user is admin
def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first","warning")
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user:
            return redirect(url_for('logout'))
        if user.is_admin == False:
            flash("You are not allowed to access this page","warning")
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return inner


@app.route('/')
@app.route('/home')
@auth_required
def home():
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('logout'))
    if user.is_admin:
        return redirect(url_for('admin'))
    lots = Lot.query.all()
    history = Reserve.query.filter_by(user_id = user.user_id)
    return render_template("user_dashboard.html",lots = lots, history = history)


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
            session['user_id'] = new_user.user_id
            flash("Welcome, "+new_user.name+"!", "success")
            return redirect(url_for('home'))
        
    return render_template("signup.html")


@app.route('/profile',methods=['GET','POST'])
@auth_required
def profile():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        name = request.form.get('name')
        cpass = request.form.get('cpassword')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')

            #validations
        if name and cpass and pass1 and pass2:
            if check_password_hash(user.password,cpass):
                if pass1 == pass2:
                    user.name = name
                    user.password = generate_password_hash(pass1)
                    db.session.commit()
                    flash("Successfully updated password","success")
                    return redirect(url_for('profile'))
                else:
                    flash("Passwords do not match","error")
            else:
                flash("Incorrect password", "error")
        else:
            flash("Please fill all details","warning")  
            
    return render_template('profile.html', user = user)


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        flash("You have been logged out", "success")
    else:
        flash("You are already logged out", "warning")
    
    return redirect(url_for('login'))



@app.route('/admin')
@admin_required
def admin():
    lots = Lot.query.all()
    return render_template("admin_dashboard.html", lots = lots)

@app.route('/admin/lot/add-lot', methods=['GET','POST'])
@admin_required
def add_lot():
    if request.method == "POST":
        prime_loc = request.form.get('prime_loc')
        address = request.form.get('address')
        pin = request.form.get('pin')
        max_spots = request.form.get('max_spots')
        price = request.form.get('price')
        is_shaded = 'is_shaded' in request.form

        if prime_loc and address and pin and max_spots and price:
            if is_shaded:
                new_lot=new_lot = Lot(prime_loc = prime_loc, address=address, pincode = pin, max_spots = max_spots, price_per_hr = price, is_shaded = True)
            else:
                new_lot = Lot(prime_loc = prime_loc, address=address, pincode = pin, max_spots = max_spots, price_per_hr = price)
            db.session.add(new_lot)
            db.session.flush()

            for i in range(int(max_spots)):
                new_spot = Spot(lot_id = new_lot.lot_id)
                db.session.add(new_spot)
            

            db.session.commit()
            flash("Parking lot created successfuly!", "success")
            return redirect(url_for("admin"))
        
        flash("Please fill out all fields","warning")

    return render_template("new_lot.html")

@app.route('/admin/lot/<int:lot_id>/edit-lot', methods=['GET','POST'])
@admin_required
def edit_lot(lot_id):
    lot = Lot.query.get(lot_id)
    if lot:
        if request.method == "POST":
            prime_loc = request.form.get('prime_loc')
            address = request.form.get('address')
            pin = request.form.get('pin')
            max_spots = request.form.get('max_spots')
            price = request.form.get('price')
            is_shaded = 'is_shaded' in request.form

            if prime_loc and address and pin and max_spots and price:
                lot.prime_loc = prime_loc
                lot.address = address
                lot.pincode = pin
                lot.max_spots = max_spots
                lot.price_per_hr = price
                if is_shaded:
                    lot.is_shaded = True
                else:
                    lot.is_shaded = False
                db.session.flush()
                
                spots_before = Spot.query.filter_by(lot_id = lot_id).all()
                max_before = len(spots_before)
                if int(max_spots) > max_before:
                    for i in range(int(max_spots) - max_before):
                        new_spot = Spot(lot_id = lot_id)
                        db.session.add(new_spot)
                elif int(max_spots) < max_before:
                    for spot in spots_before[int(max_spots):]:
                        db.session.delete(spot)
                
                db.session.commit()
                flash("Parking lot details updated successfuly!", "success")
                return redirect(url_for("admin"))
        
            flash("Please fill out all fields","warning")
    else:
        flash("Lot not found","error")
        return redirect(url_for('admin'))

    return render_template("edit_lot.html", lot = lot)


@app.route('/lot/<int:lot_id>')
@auth_required
def view_lot(lot_id):
    lot = Lot.query.get(lot_id)
    if lot:
        return render_template("view_lot.html", lot = lot)
    else:
        flash("Lot not found","error")
        return redirect(url_for('admin'))



@app.route('/admin/lot/<int:lot_id>/delete-lot')
@admin_required
def delete_lot(lot_id):
    lot = Lot.query.get(lot_id)
    if lot:
        reservation = Reserve.query.filter_by(lot_id = lot_id,is_ongoing = True).first()
        if reservation:
            flash("Cannot delete a lot that has been occupied","error")
            return redirect(url_for('admin'))
        
        db.session.delete(lot)
        db.session.commit()
        flash("Lot #"+str(lot_id)+" deleted successfully!","success")
        return redirect(url_for('admin'))
    else:
        flash("Lot not found","error")
    return render_template("admin_dashboard.html")


@app.route('/admin/lot/<int:lot_id>/spot/<int:spot_id>/view')
@admin_required
def spot_details(lot_id, spot_id):
    spot = Spot.query.get(spot_id)
    reservation = Reserve.query.filter_by(spot_id = spot_id,is_ongoing = True).first()
    if spot:
        return render_template("spot_details.html", spot = spot, reservation = reservation )
    else:
        flash("Spot does not exist","error")
        return redirect(url_for('admin'))


@app.route('/admin/users')
@admin_required
def view_users():
    users = User.query.all()
    return render_template("ad_view_users.html", users = users)


@app.route('/admin/search')
@admin_required
def search():
    return render_template("admin_search.html")


@app.route('/lot/<int:lot_id>/book-lot', methods=['GET','POST'])
@auth_required
def book_lot(lot_id):
    spot = Spot.query.filter_by(lot_id = lot_id,status = 'a').first()
    if not spot:
        flash("Sorry, no spots available in this lot. Please book another lot","error")
        return redirect(url_for('home'))
    lot = Lot.query.get(lot_id)
    user = User.query.get(session["user_id"])
    if request.method == 'POST':
        vehicle_num = request.form.get('vno')
        reservation = Reserve(user_id = user.user_id,lot_id = lot_id, spot_id = spot.spot_id, price_per_hr = lot.price_per_hr, vehicle_num = vehicle_num)
        spot.status = 'o'
        db.session.add(reservation)
        db.session.commit()

        flash("Successfully Booked Parking spot", "success")
        return redirect(url_for('home'))
    return render_template("book_spot.html", spot = spot, lot = lot, user = user)


@app.route('/lot/<int:lot_id>/spot/<int:spot_id>/release-spot', methods=['GET','POST'])
@auth_required
def release_spot(lot_id,spot_id):
    reservation = Reserve.query.filter_by(spot_id = spot_id, is_ongoing = True).first()
    if not reservation:
        flash("Spot isn't occupied or doesn't exist","error")
        return redirect('home')
    
    if request.method == 'POST':
        form_end_time = request.form.get('end_time')
        cost = int(request.form.get('cost'))
        end_time = datetime.strptime(form_end_time, "%d-%m-%y %H:%M:%S")
        reservation.end_time = end_time
        db.session.commit()
        if cost == 0:
            reservation.is_ongoing = False
            spot = Spot.query.get(spot_id)
            spot.status = 'a'
            db.session.commit()
            flash("Released Parking Spot. Have a great day.","success")
            return redirect(url_for('home'))
        payment = Payment(r_id = reservation.r_id, total_amt = cost)
        db.session.add(payment)
        db.session.commit()
        flash("Please pay ₹ "+str(cost)+" to release parking spot.","success")
        return redirect(url_for('payment', p_id = payment.payment_id))

    time_now = datetime.now()
    time_occupied = (time_now - reservation.start_time).total_seconds()/3600
    cost = round(reservation.price_per_hr * time_occupied)
    time_now_form = time_now.strftime("%d-%m-%y %H:%M:%S")
    return render_template("release_spot.html", reservation = reservation, time_now = time_now_form, cost = cost)

@app.route('/payment/<int:p_id>',methods=['GET','POST'])
@auth_required
def payment(p_id):
    payment = Payment.query.get(p_id)
    reservation = Reserve.query.get(payment.r_id)

    if request.method == 'POST':
        reservation.is_ongoing = False
        spot = Spot.query.get(reservation.spot_id)
        spot.status = 'a'
        db.session.commit()
        flash("Released Parking Spot. Have a great day.","success")
        return redirect(url_for('home'))

    return render_template("payment.html", reservation = reservation, payment = payment)
    
