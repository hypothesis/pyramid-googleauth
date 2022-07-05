from functools import lru_cache

from pyramid.authentication import SessionAuthenticationHelper


class GoogleSecurityPolicy:
    @property
    @lru_cache(maxsize=1)
    def session(self):
        return SessionAuthenticationHelper(prefix="googleauth.")

    def identity(self, request):  # pragma: no cover
        raise NotImplementedError()

    def authenticated_userid(self, request):
        return self.session.authenticated_userid(request)

    def permits(self, request, context, permission):  # pragma: no cover
        raise NotImplementedError()

    def remember(self, request, userid, **kwargs):
        return self.session.remember(request, userid, **kwargs)

    def forget(self, request, **kwargs):
        return self.session.forget(request, **kwargs)
