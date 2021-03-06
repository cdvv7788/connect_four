from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from .helpers import set_cookie
from .models import Game


class PickUser(TemplateView):
    """
    Renders a small form for the user to select a username.
    This username will be used to query the game state later.
    Find an unfinished game where the user is the participant if there is one.
    Find an unfinished game where there is no second player.
    Create a new game if there is none yet, and assign the player to the player_1 id.
    The user is added to a cookie, and that will be used to provide
    a very rudimentary matchmaking.
    """

    template_name = "create_user.html"

    def post(self, request):
        player_name = request.POST["player-name"]
        current_game = Game.objects.find_game(player_name)
        response = redirect(reverse("game", kwargs={"game_id": current_game.id}))
        set_cookie(response, "username", player_name)
        return response


class GameView(TemplateView):
    """
    Does nothing beyond rendering the game template.
    The websockets connection will be established in this page, and everything
    else will be handled that way from there on.
    """

    template_name = "play_game.html"
