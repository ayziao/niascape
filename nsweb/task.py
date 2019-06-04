from flask import Blueprint, render_template, request, redirect, flash, url_for
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


@bp.route('/create', methods=('GET', 'POST'))
# @login_required
def create():
	defaultowner = '未定'
	defaulttag = request.args.get('tag', '')

	if request.method == 'POST':
		owner = request.form['owner']
		title = request.form['title']
		tag = ' ' + request.form['tag'].strip() + ' '
		body = request.form['body']
		error = None

		if not title:
			error = 'Title is required.'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO task ("所有者", "タスク名", "タグ", "備考")'
				' VALUES (?, ?, ?, ?)',
				(owner, title, tag, body)
			)
			db.commit()
			return redirect(url_for('task.index'))

	return render_template('task/create.html', defaultowner=defaultowner, defaulttag=defaulttag)
