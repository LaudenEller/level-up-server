"""Module for generating events by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all events along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                    g.title AS game_title, e.description AS event_description,
                    e.date, e.time, gm.id AS gamer_id,
                    au.first_name || " " || au.last_name AS "full_name"
                    FROM levelupapi_gamer gm
                    JOIN levelupapi_game g 
                        ON gm.id = g.gamer_id
                    JOIN levelupapi_event e
                        ON e.game_id = g.id
                    JOIN auth_user au
                        ON au.id = gm.user_id
            """)
            
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each event.
            # This will be the structure of the events_by_user list:
            
# [
#   {
#     "gamer_id": 1,
#     "full_name": "Molly Ringwald",
#     "events": [
#       {
#         "id": 5,
#         "date": "2020-12-23",
#         "time": "19:00",
#         "game_name": "Fortress America"
#       }
#     ]
#   }
# ]

            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called event that includes 
                # the name, description, number_of_players, maker,
                # event_type_id, and skill_level from the row dictionary
                event = {
                    'description': row['event_description'],
                    'date': row['date'],
                    'time': row['time']
                }
                
                # See if the gamer has been added to the events_by_user list already
                user_dict = None
                for user_event in events_by_user:
                     if user_event['gamer_id'] == row['gamer_id']:
                         user_dict = user_event
                
                
                if user_dict:
                    # If the user_dict is already in the events_by_user list, append the event to the events list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the events_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
