SELECT * FROM levelupapi_gametype;
SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;

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