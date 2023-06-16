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

    # TODO -- write tests for every view function / feature!

