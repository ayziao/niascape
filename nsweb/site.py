from flask import Blueprint, render_template, request, redirect, flash, url_for, abort, g, current_app
from nsweb.db import get_db
from nsweb.auth import login_required

bp = Blueprint('site', __name__)


@bp.route('/@<site>')
def timeline(site):
	from niascape.usecase import timeline
	datalist = timeline({'site': site})
	return render_template('site/timeline.html', datalist=datalist)


@bp.route('/@<site>/')
def command(site):
	tag = request.args.get('tag', '')
	if tag:
		return tagtimeline(site, tag)
	body = request.args.get('searchbody', '')
	if body:
		return searchbody(site, body)

	abort(404, "Not Found" + site)


def tagtimeline(site, tag):
	from niascape.usecase import tagtimeline
	datalist = tagtimeline({'site': site, 'tag': tag})
	return render_template('site/timeline.html', datalist=datalist)


def searchbody(site, body):
	from niascape.usecase import searchbody
	datalist = searchbody({'site': site, 'searchbody': body})
	return render_template('site/timeline.html', datalist=datalist)


@bp.route('/@<site>/<hogehoge>')
def kobetu(site, hogehoge):
	abort(404, "Not Found" + site + hogehoge)
