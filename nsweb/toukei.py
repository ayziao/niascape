import json

from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from nsweb.db import get_db

bp = Blueprint('toukei', __name__, url_prefix='/toukei')


@bp.route('')
def index():
	return 'toukei index'


@bp.route('/daycount')
def daycount():
	from niascape.usecase import site
	from niascape.usecase import postcount

	sites = site.list({})

	search = {}
	search['site'] = request.args.get('site', sites[0]['site'])
	search['tag'] = request.args.get('tag', '')
	search['body'] = request.args.get('body', '')

	tags = postcount.tag({'site': search['site']})
	daycounts = postcount.day({'site': search['site'], 'tag': search['tag'], 'search_body': search['body']})

	return render_template('toukei/daycount.html', search=search, sites=sites, tags=tags ,counts=daycounts)
