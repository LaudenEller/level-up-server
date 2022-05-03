"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError

class GameView(ViewSet):
    """Level up game view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single game 
        
        Returns:
            Response -- JSON serialized game
        """
        
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all games
        
        Returns:
            Response -- JSON serialized list of game types
        """
        
        games = Game.objects.all()
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
            
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # game_type_id = request.data.game_type
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        # serializer.save(game_type_id=game_type_id)
        # game = Game.objects.create(
        #     title=request.data["title"],
        #     maker=request.data["maker"],
        #     number_of_players=request.data["number_of_players"],
        #     skill_level=request.data["skill_level"],
        #     gamer=gamer,
        #     game_type=game_type
        # )
        # serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CreateGameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type')

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    
    class Meta:
        model = Game
        depth = 2 # INSQ: This will embed all the data the client is 
                            # looking for so that the relevant objects themselves are returned instead of just the FK ids
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type')