@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('public/signup.html', message="Email already registered, please log in.")

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('public/login.html', message="You have signed up successfully, log in now.")

    return render_template('public/signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return render_template('public/index.html', message="You have signed in successfully!")
        else:
            return render_template('public/login.html', message="Seems like you haven't signed up yet, sign up now.")

    return render_template('public/login.html')
