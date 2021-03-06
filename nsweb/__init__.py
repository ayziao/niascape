import os
import datetime
from flask import Flask, Markup


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'nsweb.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import task
	app.register_blueprint(task.bp)

	# niascape
	from . import site
	app.register_blueprint(site.bp)

	from . import toukei
	app.register_blueprint(toukei.bp)

	@app.route('/hello')
	def hello_world():
		return 'Hello, World!'

	@app.route('/')
	def index():
		return 'index'

	@app.template_filter('linebreaksbr')
	def linebreaksbr(arg):
		return Markup(arg.replace('\n', '<br>'))

	@app.template_filter()
	def jptime(dt, format='%Y-%m-%d %H:%M:%S'):
		u"""utcの時間を日本時間で指定されたフォーマットで文字列化する."""
		local = datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)
		return local.strftime(format)

	return app
