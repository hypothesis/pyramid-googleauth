from pyramid_googleauth._routes import add_routes


def includeme(config):  # pragma: no cover
    add_routes(config)
