from django.db import models
# from django.forms import DateField, TimeField
import datetime

class Event(models.Model):
    
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')
    description = models.TextField()
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", related_name="attendees") # INSQ: does this set up an events column on the Gamer table?
    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value   