from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import hashlib
import datetime


db = SQLAlchemy()
app = Flask(__name__)
login_manager = LoginManager()


from .models import *
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
	return User.get_by_id(user_id)

@app.errorhandler(401)
def page_not_found(error):
    return render_template('error.html', error = 401)

@app.errorhandler(404)
def page_not_authorized(error):
    return render_template('error.html', error = 404)

@app.before_request
def before_request():
	print('')

@app.after_request
def after_request(response):
	print('')
	return response

@app.route('/')
def index():
	return redirect(url_for('login'))

@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		if  not request.form['id'] or not request.form['password']:
			return render_template('login.html',
				valid_fields = 'Campos vacios'
				)

		else:
			user = User.query.filter_by(id = request.form['id']).first()

			if user is None:
				return render_template('login.html',
					valid_fields = 'Usuario inexistente'
					)

			else:
				form_password = hashlib.md5(bytes(request.form['password'],
					encoding='utf-8')).hexdigest()

				if not form_password == user.password:
					return render_template('login.html',
						valid_fields = 'Contraseña incorrecta'
						)

				else:
					login_user(user)

					if user.type_user == 'Mozo':
						return redirect(url_for('order'))

					elif user.type_user == 'Cocinero':
						return redirect(url_for('token'))

	else:
		return render_template('login.html',
			valid_fields = ''
			)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/waiter/order', methods = ['GET','POST'])
@login_required
def order():
	if not current_user.type_user == 'Mozo':
		return render_template('error.html', error = 401)

	else:
		item_list = []
		total_price = 0
		print(item_list)

		if request.method == 'POST':
			if request.form['submit_button'] == 'Agregar Item':
				print('----------------ADD ITEM BUTTON')

				product = Product.query.filter_by(num_product = request.form['add_item']).first()

				total_price += product.unit_price
				item_list.append(Item(
					num_product = product.num_product,
					price = product.unit_price,
					state = 'Pendiente'
					))

				return render_template('order.html',
					products = Product.query.all(),
					valid_fields = '',
					user = current_user,
					items = item_list
					)

			elif request.form['submit_button'] == 'Crear pedido':
				print('----------------CREAR ORDER BUTTON')

				if  not request.form['table'] or item_list is None:
					return render_template('order.html',
						products = Product.query.all(),
						valid_fields = 'Completar el pedido',
						items = item_list,
						user = current_user
						)

				else:
					num_order = Order.query.all()[-1].num_order + 1
					for i in item_list:
						total_price += i.unit_price

					new_order = Order(
						date = datetime.datetime.now(),
						total_price = total_price,
						paid = 0,
						remark = request.form['remark'],
						dni_mozo = current_user.id,
						table = request.form['table']
						)

					for item in item_list:
						item.num_order = num_order
						db.session.add(item)
					
					db.session.add(new_order)
					db.session.commit()

					redirect(url_for('order'))

				return render_template('order.html',
					products = Product.query.all(),
					valid_fields = '',
					user = current_user,
					items = item_list
					)

		else:
			return render_template('order.html',
				products = Product.query.all(),
				valid_fields = '',
				user = current_user,
				items = item_list
				)

@app.route('/waiter/list', methods = ['GET','POST'])
@login_required
def list():
	if not current_user.type_user == 'Mozo':
		return render_template('error.html', error = 401)

	else:
		if request.method == 'POST':
			if not request.form['option']:
				return render_template('list.html',
					orders = Order.query.all(),
					order_select = None,
					valid_fields = 'Elegir un pedido',
					user = current_user
					)

			else:
				order_select = Order.query.get(request.form['option'])
				return render_template('list.html',
					orders = Order.query.all(),
					order_select = order_select,
					valid_fields = '',
					user = current_user
					)

		else:
			return render_template('list.html',
				orders = Order.query.all(),
				order_select = None, 
				valid_fields = '',
				user = current_user
				)

@app.route('/chef/token', methods = ['GET','POST'])
@login_required
def token():
	if not current_user.type_user == 'Cocinero':
		return render_template('error.html', error = 401)

	else:
		if request.method == 'POST':
			if not request.form['option']:
				return render_template('token.html',
					orders = Order.query.all(),
					order_select = None,
					valid_fields = 'Elegir un pedido',
					user = current_user
					)

			elif request.form['submit_button'] == 'Listo':
				item_select = Item.query.filter_by(num_item = request.form['token_option']).first()
				item_select.state = 'Listo'
				db.session.commit()
				return render_template('token.html',
					orders = Order.query.all(),
					order_select = None,
					valid_fields = '',
					user = current_user
					)

			else:
				order_select = Order.query.get(request.form['option'])
				return render_template('token.html',
					orders = Order.query.all(),
					order_select = order_select,
					valid_fields = '',
					user = current_user
					)

		else:
			return render_template('token.html',
				orders = Order.query.all(),
				order_select = None, 
				valid_fields = '',
				user = current_user
				)


def create_app(config):
	app.config.from_object(config)
	login_manager.init_app(app)

	with app.app_context():
		db.init_app(app)
		db.create_all()

	return app