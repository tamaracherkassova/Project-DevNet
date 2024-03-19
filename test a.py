def register():
    if request.method == "POST":
        try:
            username = request.form['username']
            password = request.form['password']

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Произошла ошибка: {e}"
    else:
        try:
            return render_template('register.html')
        except Exception as e:
            return f"Произошла ошибка: {e}"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        try:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect('/profile')
            else:
                return "Неверные учетные данные"
        except Exception as e:
            return f"Произошла ошибка: {e}"
    else:
        try:
            return render_template('login.html')
        except Exception as e:
            return f"Произошла ошибка: {e}"

@app.route('/profile')
def profile():
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)

            if user:
                total_price = sum(cart_item.item.price * cart_item.quantity for cart_item in user.cart_items)
                return render_template('profile.html', user=user, total_price=total_price)
            else:
                return "Пользователь не найден"
        else:
            return redirect('/login')
    except Exception as e:
        return f"Произошла ошибка: {e}"

@app.route('/logout')
def logout():
    try:
        session.pop('user_id', None)
        return redirect('/')
    except Exception as e:
        return f"Произошла ошибка: {e}"
