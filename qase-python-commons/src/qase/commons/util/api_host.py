from typing import Optional

DEFAULT_HOST = 'qase.io'

# Enterprise hosts share the `api-<name>.qase.io` shape but serve the web app on
# `<name>.qase.io`, so a cluster cannot be inferred from the API hostname and has
# to be listed explicitly.
CLUSTER_APP_HOSTS = {
    'api-eu.qase.io': 'app-eu.qase.io',
}


def resolve_cluster_app_url(host: str) -> Optional[str]:
    """Return the web app URL of a known Qase cluster, or None for any other host."""
    # Mirrors how a host fragment becomes the API base URL: `https://api-<host>`.
    app_host = CLUSTER_APP_HOSTS.get(f'api-{host}'.lower())
    return f'https://{app_host}' if app_host else None


def get_web_app_url(host: str) -> str:
    """Return the Qase web app base URL for the `testops.api.host` value."""
    if host == DEFAULT_HOST:
        return f'https://app.{DEFAULT_HOST}'
    return resolve_cluster_app_url(host) or f'https://{host}'
