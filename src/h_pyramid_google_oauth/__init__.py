from h_pyramid_google_oauth.routes import add_routes
from h_pyramid_google_oauth.security import GoogleSecurityPolicy
from h_pyramid_google_oauth.services import GoogleAuthService, SignatureService


def includeme(config):  # pragma: no cover
    config.register_service(
        SignatureService(
            secret=config.registry.settings["h_pyramid_google_oauth.secret"]
        ),
        iface=SignatureService,
    )
    config.register_service_factory(
        "h_pyramid_google_oauth.services.google_auth.factory", iface=GoogleAuthService
    )

    add_routes(config)
