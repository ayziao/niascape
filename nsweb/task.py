from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
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


def get_task(id, check_author=True):
	db = get_db()

	task = db.execute(
		'SELECT *'
		' FROM task'
		' WHERE "連番" = ?',
		(id,)
	).fetchone()

	if task:
		return task

	abort(404, "task id {0} doesn't exist.".format(id))
	return task


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
def update(id):
	task = get_task(id)

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
				'UPDATE task SET "所有者" = ?, "タスク名" = ?, "タグ" = ?, "備考" = ?, "変更日時" = datetime("now", "utc")'
				' WHERE "連番" = ?',
				(owner, title, tag, body, id)
			)
			db.commit()
			return redirect(url_for('task.index'))

	return render_template('task/update.html', task=task)
