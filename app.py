from flask import Flask, render_template, request, redirect, url_for
import uuid  

app = Flask(__name__)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if email in users:
            return "User already exists!"
        users[email] = {'name': name, 'password': password}
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        if user and user['password'] == password:
            return redirect(url_for('home'))
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/seats', methods=['GET'])
def seats():
    movie = request.args.get('movie')
    price = request.args.get('price')
    time = request.args.get('time')
    location = request.args.get('location')
    return render_template('seats.html', movie=movie, price=price, time=time, location=location)

@app.route('/confirm', methods=['POST'])
def confirm():
    movie = request.form.get('movie')
    location = request.form.get('location')
    time = request.form.get('time')
    seats = request.form.get('seats')
    price = request.form.get('price')
    print("DEBUG:", movie, seats, price, time, location)
    return render_template('confirm.html', movie=movie, location=location, time=time, seats=seats, price=price)

@app.route('/payment', methods=['POST'])
def payment():
    movie = request.form.get('movie')
    seats = request.form.get('seats')
    price = request.form.get('price')
    time = request.form.get('time')
    location = request.form.get('location')
    if not all([movie, seats, price, time, location]):
        return "Missing required parameters", 400
    return render_template('payment.html', movie=movie, seats=seats, price=price, time=time, location=location)

@app.route('/successfull', methods=['GET'])
def successfull():
    movie = request.args.get('movie')
    seats = request.args.get('seats')
    showtime = request.args.get('showtime')
    location = request.args.get('location')
    booking_id = str(uuid.uuid4())[:8].upper()
    return render_template(
        'successfull.html',
        movie=movie,
        showtime=showtime,
        seats=seats,
        location=location,
        booking_id=booking_id
    )

if __name__ == '__main__':
    app.run(debug=True)


