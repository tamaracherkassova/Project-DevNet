from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        image = request.files['image']
        if image:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filename)
        else:
            filename = None

        item = Item(title=title, price=price, description=description, image=filename)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')

@app.route('/clear_db') #функция очистки базы данных товаров
def clear_db():
    with app.app_context():
        db.session.query(Item).delete()
        db.session.commit()
    return redirect('/')

#маршрут для отображения списка товаров с возможностью фильтрации
@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '').strip()

    if keyword:
        items = Item.query.filter(Item.title.ilike(f"%{keyword}%")).order_by(Item.price).all()
    else:
        items = Item.query.order_by(Item.price).all()

    return render_template('index.html', data=items)