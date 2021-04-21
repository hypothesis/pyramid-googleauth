from pyramid_googleauth._routes import add_routes
from pyramid_googleauth.security import GoogleSecurityPolicy
from pyramid_googleauth.services import GoogleAuthService, SignatureService


def includeme(config):  # pragma: no cover
    config.register_service(
        SignatureService(secret=config.registry.settings["pyramid_googleauth.secret"]),
        iface=SignatureService,
    )
    config.register_service_factory(
        "pyramid_googleauth.services.google_auth.factory", iface=GoogleAuthService
    )

    add_routes(config)
