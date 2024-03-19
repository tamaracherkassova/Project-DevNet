# Маршрут для регистрации нового клиента
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('register.html')

#маршрут для входа в систему
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            return "Неверные учетные данные"
    else:
        return render_template('login.html')

#маршрут для выхода из системы
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

# Маршрут для добавления товара в корзину
@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if 'user_id' in session:
        user_id = session['user_id']
        item = Item.query.get(item_id)

        cart_item = CartItem(item_id=item_id, user_id=user_id, quantity=1)

        try:
            db.session.add(cart_item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return redirect('/login')