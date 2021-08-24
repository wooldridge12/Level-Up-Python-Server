import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        game_type = GameType()
        game_type.label = "Board game"
        game_type.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
            "name": "steve",
            "description": "fun to play for everyone"
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["maker"], data['maker'])
        self.assertEqual(json_response["skill_level"], data['skillLevel'])
        self.assertEqual(json_response["number_of_players"], data['numberOfPlayers'])
        self.assertEqual(json_response["name"], data['name'])
        
    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        # You have to add an ID because django is suppose to do that for you but this is a test so youll need to enter it manually.
        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.name = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.description: "fun to play for everyone"

        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f'/games/{game.id}')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], game.name)
        self.assertEqual(json_response["maker"], game.maker)
        self.assertEqual(json_response["skill_level"], game.skill_level)
        self.assertEqual(json_response["number_of_players"], game.number_of_players)
        self.assertEqual(json_response["description"], game.description)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.decription = "Not always fun"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameTypeId": 1,
            "skillLevel": 2,
            "name": "Sorry",
            "maker": "Hasbro",
            "description": "game fun",
            "numberOfPlayers": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["name"], data ['name'])
        self.assertEqual(json_response["maker"], data ['maker'])
        self.assertEqual(json_response["skill_level"], data ['skillLevel'])
        self.assertEqual(json_response["number_of_players"], data ['numberOfPlayers'])
        self.assertEqual(json_response["description"], data ['description'])

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.description = "some cool description"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
