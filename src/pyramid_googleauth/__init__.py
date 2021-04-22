from pyramid_googleauth._routes import add_routes as _add_routes
from pyramid_googleauth.security import GoogleSecurityPolicy


def includeme(config):  # pragma: no cover
    _add_routes(config)
