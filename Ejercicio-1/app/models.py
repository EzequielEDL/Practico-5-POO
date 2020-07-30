from . import db
import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	password = db.Column(db.String(32), nullable = False)
	type_user = db.Column(db.String(4), nullable = False)
	#order = db.relationship('User', backref = 'orders',
	#	cascade = "all, delete-orphan", lazy = 'dynamic')

	def __str__(self):
		return '|' +\
			str(self.id) + '|' +\
			str(self.type_user) + '|'

	@classmethod
	def get_by_id(cls, id):
		return User.query.filter_by(id = id).first()
		

class Product(db.Model):
	__tablename__ = 'products'
	num_product = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), unique = True, nullable = False)
	unit_price = db.Column(db.Float, nullable = False)
	item = db.relationship('Item', backref = 'products',
		cascade = "all, delete-orphan", lazy = 'dynamic')

	def __str__(self):
		return \
			str(self.num_product) + ': $' +\
			str(self.unit_price).replace('.', ',') + ' - ' +\
			str(self.name)


class Item(db.Model):
	__tablename__ = 'items'
	num_item = db.Column(db.Integer, primary_key = True)
	num_order = db.Column(db.Integer, db.ForeignKey('orders.num_order'))
	num_product = db.Column(db.Integer, db.ForeignKey('products.num_product'))
	price = db.Column(db.Float, nullable = False)
	state = db.Column(db.String(10), nullable = False)

	def __str__(self):
		return '$' +\
			str(self.price).replace('.', ',') + ' - ' +\
			str(self.__get_by_num_product()) + ' | ' +\
			str(self.state)

	def __get_by_num_product(self):
		return Product.query.filter_by(num_product = self.num_product).first().name


class Order(db.Model):
	__tablename__ = 'orders'
	num_order = db.Column(db.Integer, primary_key = True)
	date = db.Column(db.DateTime, nullable = False)
	total_price = db.Column(db.Float, nullable = False)
	paid = db.Column(db.Integer, nullable = False)
	remark = db.Column(db.Text)
	dni_mozo = db.Column(db.Integer, nullable = False)
	table = db.Column(db.Integer, nullable = False)
	item = db.relationship('Item', backref = 'orders',
		cascade = "all, delete-orphan", lazy = 'dynamic')
	#id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __str__(self):
		if self.paid == 1: paid = 'Cobrado'
		else: paid = 'Sin cobrar'
		return '$' +\
			str(self.total_price).replace('.', ',') + ': ' +\
			paid + ' - ' +\
			str(self.remark) + ' - ' +\
			str(self.date)


	def get_by_state(self):
		eva_state = 'Pendiente'
		item = self.item.filter_by(state = eva_state).first()

		if item is not None:
			return True

		else:
			return False
		
'''
	#Producto
	+	NumProducto: entero
	+	Nombre: cadena
	+	PrecioUnitario: real
	+	Items: * #Item

	#Item
	+	Numitem: entero
	+	Precio: real
	+	Estado: cadena
	+	Producto: #Producto
	+	Pedido: #Pedido

	#Pedido
	+	NumPedido: entero
	+	Fecha: fecha
	+	Total: real
	+	Cobrado: booleano
	+	Observacion: cadena
	+	idMozo: entero
	+	Mesa: entero
	+	Items: * #Item
	+	Usuario: #Usuario

	#Usuario
	+	id: entero
	+	Clave: cadena
	+	Tipo: cadena
	+	Pedido: * #Pedido
'''