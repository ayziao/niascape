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
	sites = site.list({})
	return render_template('toukei/daycount.html', sites=sites)
