import sqlite3
from django.shortcuts import render
from levelupapi.models import Game
from levelupreports.views import Connection

def events_by_user(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all events, with related user info.
            db_cursor.execute("""
                SELECT 
                    g.id as user_id, 
                    u.first_name || " " || u.last_name as full_name, 
                    e.id, 
                    e.date, 
                    e.time, 
                    gm.name
                FROM 
                    levelupapi_event e
                JOIN 
                    levelupapi_eventgamer eg on e.id = eg.event_id
                JOIN 
                    levelupapi_gamer g on g.id = eg.gamer_id
                JOIN 
                    auth_user u on u.id = g.user_id
                JOIN 
                    levelupapi_game gm on e.game_id = gm.id
            """)

            dataset = db_cursor.fetchall()

            events_by_user = {}

            for row in dataset:
                uid = row['id']
                if uid in events_by_user:
                    events_by_user[uid]['events'].append({
                        "id": row['id'],
                        "date": row["date"],
                        "time": row["time"],
                        "game_name": row["name"]
                    })
                else:
                    events_by_user[uid] = {
                        "gamer_id": uid,
                        "full_name": row['full_name'],
                        "events": [{
                            "id": row['id'],
                            "date": row["date"],
                            "time": row["time"],
                            "game_name": row["name"]
                        }]
                    }

            events = events_by_user.values()
            context = { "user_with_events": events }
            template = "users/list_with_events.html"
            return render(request, template, context)