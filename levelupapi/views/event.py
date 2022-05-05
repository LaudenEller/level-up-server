"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError


# INSQ: The EventView class parses an HTTP request and uses ORM to return the requested data

class EventView(ViewSet):
    """Level up event view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single event type
        
        Returns:
            Response -- JSON serialized event
        """
       
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all events
        
        Returns:
            Response -- JSON serialized list of event types
        """
        
        event = Event.objects.all() # INSQ: This is ORM, it returns all the Event objects in the db
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized event instance
        """
        
        organizer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # organizer = gamer.objects.get(user=request.auth.user)
        # event = event.objects.get(pk=request.data["event_id"])

        # event = Event.objects.create(
        #     description=request.data["description"],
        #     date=request.data["date"],
        #     time=request.data["time"],
        #     event=event,
        #     organizer=organizer
        # )
        # serializer = EventSerializer(event)
        # return Response(serializer.data)
        
    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
# INSQ: The EventSerializer constructs a JSON representation of the data the client requested
      
class CreateEventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'game', 'organizer')
        
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    
    class Meta:
        model = Event
        depth = 2
        fields = ('id', 'description', 'date', 'time', 'game', 'organizer')