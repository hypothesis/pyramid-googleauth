"""The routes for the Pyramid app."""


def add_routes(config):
    """Register all routes."""

    config.add_route(
        "pyramid_googleauth_login",
        config.registry.settings.get("pyramid_googleauth.login_route", "/ui/api/login"),
    )
    config.add_route(
        "pyramid_googleauth_login_callback",
        config.registry.settings.get(
            "pyramid_googleauth.login_callback_route", "/ui/api/login_callback"
        ),
    )
    config.add_route(
        "pyramid_googleauth_logout",
        config.registry.settings.get(
            "pyramid_googleauth.logout_route", "/ui/api/logout"
        ),
    )

    config.add_route(
        "pyramid_googleauth_login_failure",
        config.registry.settings.get(
            "pyramid_googleauth.login_failure_route", "/ui/api/login_failure"
        ),
    )
    config.scan()
