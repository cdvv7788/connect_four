from django.views.generic import TemplateView


class LobbyView(TemplateView):
    """
    Renders lobby with all online players
    """

    template_name = "lobby.html"
