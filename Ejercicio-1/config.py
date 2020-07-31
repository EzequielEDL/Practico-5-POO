
class Default():
	SECRET_KEY = "GDtfDCFYjD"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Default):
	DEBUG = True

config = {
	'development': DevelopmentConfig,
	'default': Default
}
		