"""Flask app to handle server-side game logic; including HTTP requests, sessions to store data between requests, and Jinja templates to render HTML. Implements the Boggle game logic in the boggle module, and the Flask routes handle the interactions with the game logic and data storage."""


from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

#creates flask app instance and assigns it to the app variable
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

#creates a boggle game instance and assigns it to the boggle_game variable that will beused to generate the boggle board and check the validity of the words
boggle_game = Boggle()

#define the home/homepage route that is executed when a request is made to the home route
@app.route("/")
def home():

    """Make the board"""
    #generate the boggle game board using make_board function from boggle_game instance
    board = boggle_game.make_board()
    #store the board in session for later user
    session["board"] = board
    #retrieve highest score and number of tries from session using session.get with default values
    highest_score = session.get("highest_score", 0)
    num_tries = session.get("num_tries", 0)
  
    #render_template is used to render the home page index.html with the board and highest score and number of tries
    return render_template("index.html",board=board,
                           highest_score=highest_score, num_tries=num_tries)
  
#define the route to check the validity of the words
@app.route("/check-word")
def check_word():
    """ Check the validity of the words; if found in dictionary"""

    #word is extracted from the request arguments and board is retrieved from session
    #check_validity method is used from the boggle_game instance to check the validity of the word on the board
    word = request.args.get("word")
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    #result is returned as json
    return jsonify({"result" : response})

#define the route to make a POST request to receive the score and update the highest score if applicable
@app.route("/post-score", methods=["POST"])
def post_score():
    """ Retrieve the score and update the highest score if applicable"""
    #score is extracted from JSON data in the request
    score = request.get.json()["score"]
    #highest_score is retrieved from session
    highest_score = session.get("highest_score", 0)
    #update the session and number of tries
    num_tries = session.get("num_tries", 0)

    #update the session with the new score and number of tries
        #the number of tries is incremented by 1 and stored in session
        #the highest score is updated by taking the maxiumum of the current score and the stored high school
    session["num_tries"] = num_tries + 1
    session["highest_score"] = max(score, highest_score)

    #return the response as json object if a new highest score has been found.
        #return json object with the key "isNewRecord" to indicate the score is greater than the highest score
    return jsonify(isNewRecord=score > highest_score)

