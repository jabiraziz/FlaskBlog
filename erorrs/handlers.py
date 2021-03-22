from flask import Blueprint, render_template

# Create Blueprint
errors = Blueprint('erorrs', __name__)


# page not found error
@errors.app_errorhandler(404)
def error_404(error):
    """2nd argument in return statement will help ot get the
    correct-error code respond."""
    return render_template('404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


# error 500: means something has gone wrong on the web site's server (Generall server error)
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500
