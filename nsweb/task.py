from flask import Blueprint, render_template, request, redirect, flash, url_for, abort, g, current_app
from nsweb.db import get_db
from nsweb.auth import login_required

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('')
def index():
	stars = ['☆☆☆☆☆', '★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★']
	tags = {}

	search = {
		'owner': request.args.get('owner', ''),
		'rate': request.args.get('rate', ''),
		'tag': request.args.get('tag', '')}
	sort = request.args.get('sort', '')

	where = ''
	if search['owner']:
		where += ' "所有者" = "' + search['owner'] + '" '
	if search['rate']:
		if where:
			where += ' AND '
		where += ' "重要度" <= "' + search['rate'] + '" '
	if search['tag']:
		if where:
			where += ' AND '
		where += ' "タグ" like "% ' + search['tag'] + ' %" '
	if where:
		where = ' WHERE ' + where

	order = ' ORDER BY "状態" DESC, CASE "重要度" WHEN 0 THEN 9 ELSE "重要度" END DESC, "完了日時" DESC, "連番" DESC'
	if sort == 'time':
		order = ' ORDER BY "状態" DESC, "完了日時" DESC, "連番" DESC'

	sql = 'SELECT * FROM task' + where + order
	rows = get_db().execute(sql).fetchall()

	# current_app.logger.debug(sql)

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

	return render_template('task/index.html', tasks=tasks, tags=tags, stars=stars, search=search, sort=sort)


@bp.route('/create', methods=('GET', 'POST'))
def create():
	defaultowner = g.user['username'] if g.user else '未定'
	defaultowner = request.args.get('owner', defaultowner)
	defaulttag = request.args.get('tag', '')

	if request.method == 'POST':
		owner = request.form['owner'] if request.form['owner'] else defaultowner
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
			if request.form['ret'] == 'on':
				return redirect(url_for('task.index', owner=owner, tag=tag.strip()))
			else:
				return redirect(url_for('task.index'))

	return render_template('task/create.html', defaultowner=defaultowner, defaulttag=defaulttag)


def get_task(number, check_author=True):
	db = get_db()

	task = db.execute(
		'SELECT *'
		' FROM task'
		' WHERE "連番" = ?',
		(number,)
	).fetchone()

	if task is None:
		abort(404, "task id {0} doesn't exist.".format(number))

	return task


def get_args():
	args = {
		'owner': request.args.get('owner', ''),
		'rate': request.args.get('rate', ''),
		'tag': request.args.get('tag', ''),
		'sort': request.args.get('sort', '')}
	return args


@bp.route('/<int:number>/update', methods=('GET', 'POST'))
# @login_required
def update(number):
	task = get_task(number)

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
				(owner, title, tag, body, number)
			)
			db.commit()
			return redirect(url_for('task.index'))

	return render_template('task/update.html', task=task)


@bp.route('/<int:number>/delete', methods=('POST',))
@login_required
def delete(number):
	get_task(number)
	db = get_db()
	db.execute('DELETE FROM task WHERE "連番" = ?', (number,))
	db.commit()
	return redirect(url_for('task.index'))


@bp.route('/<int:number>/rateup', methods=('GET',))
def rateup(number):
	args = get_args()

	task = get_task(number)
	if task['重要度'] < 5:
		db = get_db()
		db.execute(
			'UPDATE task SET "重要度" = "重要度" + 1 '
			' WHERE "連番" = ?', (number,))
		db.commit()

		if args['rate'].isnumeric():
			args['rate'] = int(args['rate']) + 1

	return redirect(url_for('task.index', **args))


@bp.route('/<int:number>/ratedown', methods=('GET',))
def ratedown(number):
	args = get_args()

	task = get_task(number)
	if task['重要度'] > 0:
		db = get_db()
		db.execute(
			'UPDATE task SET "重要度" = "重要度" - 1 '
			' WHERE "連番" = ?', (number,))
		db.commit()

		if args['rate'].isnumeric():
			args['rate'] = int(args['rate']) - 1

	return redirect(url_for('task.index', **args))


@bp.route('/<int:number>/done', methods=('GET',))
def done(number):
	args = get_args()

	db = get_db()
	db.execute(
		'UPDATE task SET "状態" = "完" , "完了日時" = datetime("now", "utc") '
		' WHERE "連番" = ?', (number,))
	db.commit()
	return redirect(url_for('task.index', **args))


@bp.route('/<int:number>/restore', methods=('GET',))
def restore(number):
	args = get_args()

	db = get_db()
	db.execute(
		'UPDATE task SET "状態" = "未" , "完了日時" = "" '
		' WHERE "連番" = ?', (number,))
	db.commit()
	return redirect(url_for('task.index', **args))
