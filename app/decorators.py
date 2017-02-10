from functools import wraps
from flask_user.access import is_authenticated
from flask_restful import abort
from flask_login import current_user


def login_required(func):
    """ This decorator ensures that the current user is logged in before calling the actual view.
        Calls the unauthorized_view_function() when the user is not logged in."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # User must be authenticated
        if not is_authenticated():
            # Redirect to unauthenticated page
            return abort(401)

        # Call the actual view
        return func(*args, **kwargs)
    return decorated_view


def roles_required(*role_names):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.has_role(*role_names):
                # Redirect to the unauthorized page
                return 403
        return decorated_view
    return wrapper
