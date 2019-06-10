from flask import Blueprint, render_template, request, redirect, flash, url_for, abort, g, current_app
from nsweb.db import get_db
from nsweb.auth import login_required

bp = Blueprint('site', __name__)

@bp.route('/@<site>')
def sitetimeline(site):
	from niascape.usecase import timeline
	datalist = timeline({'site': site})
	return render_template('site/timeline.html', datalist=datalist)
