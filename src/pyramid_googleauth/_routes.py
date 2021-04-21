"""The routes for the Pyramid app."""


def add_routes(config):
    """Register all routes."""

    config.add_route(
        "pyramid_googleauth.login",
        config.registry.settings.get(
            "pyramid_googleauth.login_route", "/googleauth/login"
        ),
    )
    config.add_route(
        "pyramid_googleauth.login.callback",
        config.registry.settings.get(
            "pyramid_googleauth.login_callback_route", "/googleauth/login/callback"
        ),
    )
    config.add_route(
        "pyramid_googleauth.logout",
        config.registry.settings.get(
            "pyramid_googleauth.logout_route", "/googleauth/logout"
        ),
    )

    config.add_route(
        "pyramid_googleauth.login.failure",
        config.registry.settings.get(
            "pyramid_googleauth.login_failure_route", "/googleauth/login/failure"
        ),
    )
    config.scan()
