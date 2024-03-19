def index():
    try:
        items = Item.query.order_by(Item.price).all()
        item_titles = [item.title for item in items]
        total_items = len(items)
        return render_template('index.html', data=items, getCategoryName=getCategoryName, item_titles=item_titles, total_items=total_items)
    except Exception as e:
        return f"Произошла ошибка: {e}"

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        try:
            title = request.form['title']
            price = request.form['price']
            category = request.form['category']
            description = request.form['description']
            image = request.files['image']

            valid_categories = ['category1', 'category2', 'category3']
            if category not in valid_categories:
                return "Некорректная категория"

            if image:
                filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(filename)
                image_url = filename
            else:
                filename = None
                image_url = None

            item = Item(title=title, price=price, category=category, description=description, image=image_url)
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Произошла ошибка: {e}"
    else:
        try:
            return render_template('create.html')
        except Exception as e:
            return f"Произошла ошибка: {e}"

def getCategoryName(category_id):
    try:
        categories = {
            'category1': 'Одежда',
            'category2': 'Электроника',
            'category3': 'Книги'
        }

        return categories.get(category_id, 'Неизвестная категория')
    except Exception as e:
        return f"Произошла ошибка: {e}"

@app.route('/clear_db')
def clear_db():
    try:
        with app.app_context():
            db.session.query(Item).delete()
            db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Произошла ошибка: {e}"

@app.route('/search', methods=['GET'])
def search():
    try:
        keyword = request.args.get('keyword', '').strip()
        if keyword:
            items = Item.query.filter(Item.title.ilike(f"%{keyword}%")).order_by(Item.price).all()
        else:
            items = Item.query.order_by(Item.price).all()
        return render_template('index.html', data=items, getCategoryName=getCategoryName)
    except Exception as e:
        return f"Произошла ошибка: {e}"
