"""
learn flask views
"""
# pylint: disable=invalid-name, too-few-public-methods

from datetime import datetime
from flask import Flask, url_for, redirect, request, render_template, session, flash

from . import main
from .forms import NameForm
from .. import mydb
#from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    """index"""
    pyform = NameForm()
    if pyform.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('index.html', indexform=pyform,
                           indexname2=session.get('pyname'),
                           exist_index=session.get('exist', False),
                           current_time=datetime.utcnow())
