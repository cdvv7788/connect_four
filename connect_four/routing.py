from channels.routing import ProtocolTypeRouter, URLRouter
import games.routing
import presence.routing

url_patterns = (
    games.routing.websocket_urlpatterns + presence.routing.websocket_urlpatterns
)

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": URLRouter(url_patterns)
    }
)
