from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from nsweb.db import get_db

bp = Blueprint('toukei', __name__, url_prefix='/toukei')


@bp.route('')
def toukei_index():
	return 'toukei index'
