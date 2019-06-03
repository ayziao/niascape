from flask import Blueprint

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('')
def index():
	return 'task index'
