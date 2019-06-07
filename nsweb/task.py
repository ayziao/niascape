from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
from nsweb.db import get_db

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('')
def index():
	stars = ['☆☆☆☆☆', '★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★']
	search = {}
	tags = {}

	search['owner'] = request.args.get('owner', '')
	search['rate'] = request.args.get('rate', '')
	search['tag'] = request.args.get('tag', '')

	where = ''
	if search['owner']:
		where += ' "所有者" = "' + search['owner'] + '" '
	if search['rate']:
		if where:
			where += ' AND '
		where += ' "重要度" = "' + search['rate'] + '" '
	if search['tag']:
		if where:
			where += ' AND '
		where += ' "タグ" like "% ' + search['tag'] + ' %" '
	if where:
		where = ' WHERE ' + where

	db = get_db()
	rows = db.execute(
		'SELECT *'
		' FROM task' + where +
		' ORDER BY "状態" DESC, "完了日時" DESC, "連番" DESC'
	).fetchall()

	joutai = ''
	tasks = {}

	for item in rows:
		tags[item['連番']] = item['タグ'].split()
		if item["状態"] == joutai:
			tasks[item['状態']].append(item)
		else:
			joutai = item['状態']
			tasks[item['状態']] = []
			tasks[item['状態']].append(item)

	return render_template('task/index.html', tasks=tasks, tags=tags, stars=stars, search=search)


@bp.route('/create', methods=('GET', 'POST'))
# @login_required
def create():
	defaultowner = request.args.get('owner', '未定')
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

	if task is None:
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


@bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
def delete(id):
	get_task(id)
	db = get_db()
	db.execute('DELETE FROM task WHERE "連番" = ?', (id,))
	db.commit()
	return redirect(url_for('task.index'))


@bp.route('/<int:id>/rateup', methods=('GET',))
def rateup(id):
	search = {}
	search['owner'] = request.args.get('owner', '')
	search['rate'] = request.args.get('rate', '')
	search['tag'] = request.args.get('tag', '')

	task = get_task(id)
	if task['重要度'] < 5:
		db = get_db()
		db.execute(
			'UPDATE task SET "重要度" = "重要度" + 1 '
			' WHERE "連番" = ?', (id,))
		db.commit()

		if search['rate'].isnumeric():
			search['rate'] = int(search['rate']) + 1

	return redirect(url_for('task.index', **search))


@bp.route('/<int:id>/ratedown', methods=('GET',))
def ratedown(id):
	search = {}
	search['owner'] = request.args.get('owner', '')
	search['rate'] = request.args.get('rate', '')
	search['tag'] = request.args.get('tag', '')

	task = get_task(id)
	if task['重要度'] > 0:
		db = get_db()
		db.execute(
			'UPDATE task SET "重要度" = "重要度" - 1 '
			' WHERE "連番" = ?', (id,))
		db.commit()

		if search['rate'].isnumeric():
			search['rate'] = int(search['rate']) - 1

	return redirect(url_for('task.index', **search))


@bp.route('/<int:id>/done', methods=('GET',))
def done(id):
	db = get_db()
	db.execute(
		'UPDATE task SET "状態" = "完" , "完了日時" = datetime("now", "utc") '
		' WHERE "連番" = ?', (id,))
	db.commit()
	return redirect(url_for('task.index'))


@bp.route('/<int:id>/restore', methods=('GET',))
def restore(id):
	db = get_db()
	db.execute(
		'UPDATE task SET "状態" = "未" , "完了日時" = "" '
		' WHERE "連番" = ?', (id,))
	db.commit()
	return redirect(url_for('task.index'))
