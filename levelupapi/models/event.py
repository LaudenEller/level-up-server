from django.db import models
import datetime

class Event(models.Model):
    
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')
    description = models.TextField()
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", related_name="events")

    # this is an imported method (function) that adds a property === the value of the incoming value by using the .setter function
    @property # Is this a getter that collects a property from the db or a creator that adds a property
    def joined(self):
        return self.__joined
    
    #  This is a method that sets the value pair for the __joined property to the incoming value from the instantiation
    @joined.setter # This determines the value of the new property
    def joined(self, value):
        self.__joined = value   