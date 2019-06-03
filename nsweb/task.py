from flask import Blueprint, render_template
from nsweb.db import get_db

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('')
def index():
	db = get_db()

	tasks = db.execute(
		'SELECT *'
		' FROM task'
		' ORDER BY "連番" DESC'
	).fetchall()

	return render_template('task/index.html', tasks=tasks)
