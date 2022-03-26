from flask import Flask, make_response, redirect, render_template, request, url_for
from .models import db, Product, Category
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{app.instance_path}/survey.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/category')
    def get_all_category():
        category = Category.query.all()

        return render_template('category/list-category.html', category=category)
    
    @app.route('/category/form-category/<int:id>', methods=['GET', 'POST'])
    def form_category(id):
        title = ''

        if id:
            title = 'Edit Product'
        else:
            title = 'Add Product'
            
        category = {
            'id': 0,
            'name': '',
        }
            
        find_category = Category.query.filter_by(
            id=id).first()

        if find_category:
            category = find_category
        else:
            category = category
        
        if request.method == 'POST':
            if id:
                category.name = request.form['name']
                db.session.commit()
                return redirect(url_for('get_all_category'))
            else:
                name = request.form['name']
                category = Category(name=name)
                db.session.add(category)
                db.session.commit()
                return redirect(url_for('get_all_category'))
        else:
            return render_template('category/form-category.html', category=category, title=title)
    
    @app.route('/categories/remove_category/<int:id>')
    def remove_category(id):
        category = Category.query.filter_by(id=id).first()
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('get_all_category'))

    
    @app.route('/products',  methods=['GET', 'POST'])
    def get_all_product():
        category = Category.query.all()
        ct_id = 0
        
        if request.method == 'GET':
            products = Product.query.all()
        else:
            if int(request.form['category_id']) > 0:
                products = Product.query.filter_by(category_id = request.form['category_id'])
                
                if not products == []:
                    ct_id = products[0].category_id
                else:
                    products = []
            else:
                products = Product.query.all()

        return render_template('products/list-product.html', products=products, category=category, ct_id=ct_id)
    
    @app.route('/products/form-product/<int:id>', methods=['GET', 'POST'])
    def form_product(id):
        title = ''

        if id:
            title = 'Edit Product'
        else:
            title = 'Add Product'
            
        product = {
            'id': 0,
            'name': '',
            'price': 0,
            'category_id': 0,
            'category': {
                'id': 0,
                'name': ''
            }
        }
            
        find_product = Product.query.filter_by(
            id=id).first()

        if find_product:
            product = find_product
        else:
            product = product
        
        category = Category.query.all()

        if request.method == 'POST':
            if id:
                product.name = request.form['name']
                product.price = request.form['price']
                product.category_id = request.form['category_id']
                db.session.commit()
                return redirect(url_for('get_all_product'))
            else:
                name = request.form['name']
                price = request.form['price']
                category_id = request.form['category_id']
                product = Product(name=name, price=price,
                                  category_id=category_id)
                db.session.add(product)
                db.session.commit()
                return redirect(url_for('get_all_product'))
        else:
            return render_template('products/form-product.html', product=product, category=category, title=title)

    @app.route('/products/<int:id>')
    def get_product_by_id(id):
        product = Product.query.filter_by(id=id).first()

        return render_template('products/product-detail.html', product=product)

    @app.route('/products/remove_product/<int:id>')
    def remove_product(id):
        product = Product.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('get_all_product'))
    return app
