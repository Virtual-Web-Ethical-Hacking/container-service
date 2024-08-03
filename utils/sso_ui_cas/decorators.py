from functools import wraps
from fastapi.responses import RedirectResponse

from .utils import (
    get_cas_client,
    get_service_url,
    authenticate,
)


def with_sso_ui(func, force_login=True):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        service_url = get_service_url(request)
        client = get_cas_client(service_url)
        login_url = client.get_login_url()

        params = request.query_params
        if params:
            ticket = params["ticket"]
            sso_profile = authenticate(ticket, client)

            if sso_profile is None and force_login:
                return RedirectResponse(login_url)

            kwargs.update({"sso_profile": sso_profile})
            return await func(request, *args, **kwargs)
        else:
            return RedirectResponse(login_url)

    return wrapper

