class DevelopmentConfig():
	DEBUG = True
	SECRET_KEY = "GDtfDCFYjD"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig
}
		