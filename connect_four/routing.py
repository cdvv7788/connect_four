from channels.routing import ProtocolTypeRouter, URLRouter
import games.routing

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": URLRouter(games.routing.websocket_urlpatterns)
    }
)
