"""The routes for the Pyramid app."""


def add_routes(config):
    """Register all routes."""

    config.add_route(
        "h_pyramid_google_oauth_login",
        config.registry.settings.get(
            "h_pyramid_google_oauth.login_route", "/ui/api/login"
        ),
    )
    config.add_route(
        "h_pyramid_google_oauth_login_callback",
        config.registry.settings.get(
            "h_pyramid_google_oauth.login_callback_route", "/ui/api/login_callback"
        ),
    )
    config.add_route(
        "h_pyramid_google_oauth_logout",
        config.registry.settings.get(
            "h_pyramid_google_oauth.logout_route", "/ui/api/logout"
        ),
    )

    config.add_route(
        "h_pyramid_google_oauth_login_failure",
        config.registry.settings.get(
            "h_pyramid_google_oauth.login_failure_route", "/ui/api/login_failure"
        ),
    )
    config.scan()
