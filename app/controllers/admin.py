@admin_bp.route('/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_admin = AdminUser.query.filter_by(email=email).first()
        if existing_admin:
            return render_template('admin/admin_signup.html', message="Admin email already registered, please log in.")

        new_admin = AdminUser(email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()
        return render_template('admin/admin_login.html', message="Admin signed up successfully, log in now.")

    return render_template('admin/admin_signup.html')


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = AdminUser.query.filter_by(email=email, password=password).first()
        if admin:
            return render_template('admin/admin_dashboard.html', message="Admin signed in successfully!")
        else:
            return render_template('admin/admin_login.html', message="Admin not found, please sign up first.")

    return render_template('admin/admin_login.html')
