""" The test file contains unit tests for the Flask application. It tests the homepage route, word validation, and scoring functionality.

It imports the necessary modules: unittest, app from app.py, and Boggle from boggle.py.
The TestApp class inherits from unittest.TestCase and defines test methods for different aspects of the application.
The tests include checking the response status code for the homepage, checking word validation, and checking the scoring functionality.
"""

from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    """  This defines a test class named FlaskTests that inherits from TestCase. All test methods will be defined inside this class."""
    
    #define setUp method
    def setUp(self):
        """ setUp(self) is a method that is run before each test method. It sets up the test environment by creating a Flask test client and configuring the app to run in testing mode."""

        # Create a test client for the Flask application.
        self.client = app.test_client()
        # Set the TESTING configuration option of the Flask app to True.
        app.config["TESTING"] = True
    
    def test_home(self):
        """Test the home view function."""
        with self.client:
            # GET request to the home route
            response = self.client.get('/')
            
            # Assert that the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)
            
            # Assert that the 'board', 'highest_score', and 'num_tries' keys are in the session
            self.assertIn('board', session)
            self.assertIsNone(session.get('highest_score'))
            self.assertIsNone(session.get('num_tries'))
            
            # Assert that specific HTML content is present in the response
            self.assertIn(b'<p>Highest Score:', response.data)
            self.assertIn(b'Tries:', response.data)

    def test_check_word_valid(self):
        """Test the check_word view function with a valid word."""
        with self.client as client:
            # Create a session with a pre-defined board
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        
        # GET request to check-word route with a valid word 'cat'
        response = self.client.get('/check-word?word=cat')
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the result in the JSON response is 'ok'
        self.assertEqual(response.json['result'], 'ok')

    def test_check_word_invalid_on_board(self):
        """Test the check_word view function with an invalid word on the board."""
        # GET request to check-word route with an invalid word 'impossible'
        response = self.client.get('/check-word?word=impossible')
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the result in the JSON response is 'not-on-board'
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_check_word_invalid_not_word(self):
        """Test the check_word view function with an invalid word not in the dictionary."""
        # Simulate a GET request to check-word route with an invalid word 'fsjdakfkldsfjdslkfjdlksf'
        response = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the result in the JSON response is 'not-word'
        self.assertEqual(response.json['result'], 'not-word')

    def test_post_score(self):
        """Test the post_score view function."""
        with self.client as client:
            # Simulate a session with pre-defined highest_score and num_tries
            with client.session_transaction() as sess:
                sess['highest_score'] = 50
                sess['num_tries'] = 5
        
        # POST request to post-score route with a JSON payload {"score": 60}
        response = self.client.post('/post-score', json={"score": 60})
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert that isNewRecord in the JSON response is True
        self.assertTrue(response.json['isNewRecord'])
        
        # Assert that the num_tries in the session is incremented by 1
        self.assertEqual(session['num_tries'], 6)
        
        # Assert that the highest_score in the session is updated to 60
        self.assertEqual(session['highest_score'], 60)

if __name__ == '__main__':
    unittest.main()

        
        
        
        

    

