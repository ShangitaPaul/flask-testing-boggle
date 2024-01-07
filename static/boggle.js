/* JavaScript file contains the code for the Boggle game's client-side logic. It defines a BoggleGame class that handles game initialization, word submission, score calculation, timer management, and interaction with the server using AJAX requests.

The contents of this file implements the client-side functuonality*/


class BoggleGame {
    /* Initializes various properties such as game duration, score, word set, and the board element.*/

    // The class constructor takes the ID of the game board element in the HTML, and an optional game duration defaulted to 60 seconds.
    constructor(boardId, secs = 60) {
        // Assign the value of the secs parameter to the secs property of the current instance of the BoggleGame class. 
        // This represents the game length in seconds
        this.secs = secs;
        // Call the displayTimer method 
        this.displayTimer();
        
        // Initialize the score property of the current instance of the BoggleGame class to 0.
        // Thisrepresents the current player's score
        this.score = 0;
        /* Initializes the current score to 0*/

        // Create a new Set object to hold the "words"; thus, assigning it to the words property of the current instance of the BoggleGame class
        // Set is a data structure that allows us to store unique words
        this.words = new Set();
        // Select the HTML element with the ID specified by the boardId parameter using jQuery's selector method of the $ symbol
        // This allows the code to interact with the game board element
        this.board = $("#" + boardId);
        /* Stores the valid words entered by the current player*/
    
        // Set up a reoccuring timer using the setInterval method of the current instance of the BoggleGame class. 
        // setInterval is a function calls the tick method of the current instance of the BoggleGame class every 1000 milliseconds..
        // Tick method updates the timer and checks if game has ended. 
        // bind(this) is used to bind (or ensure) that tick is called on the current instance of the BoggleGame class
        this.timer = setInterval(this.tick.bind(this), 1000);
        /* Holds the timer ID for the setInterval function*/

        // Add an even listener to the submit button of the class "add-word" that is a child  of the this.board element.
        // When submit button is clicked, this.handleSubmit is called with the current instance of the BoggleGame class
        // bind(this) is used to bind (or ensure) that handleSubmit is called on the current instance
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }
    // Define displayWord method that takes a word as an argument and displays it in the game board.
    displayWord(word) {
        /* UPdates and adds a word to the word list on the UI (html)*/

        $(".words", this.board).append($("<li>", { text: word }));
    }

    displayScore() {
        /* Updates and displays the player's score on the UI (html)*/

        //Selects the element with the class "score" that is a child of the "this.board" element
        // .text(this.score) sets te text property of the selected element to the value of the score propery of the current instance. 
        $(".score", this.board).text(this.score);
    }

    statusMessage(msg, cssClass) {
        /* Dispalys a status message on the UI (html)*/

        // Selects the element with the class "msg" that is a child of the "this.board
        $(".msg", this.board)
            // Sets the text property of the selected element to the value of the msg property of the current instance
            .text(msg)
            // removes all CSS clases from the selected element 
            .removeClass()
            //Adds the class "msg" and value of "classCss" parameter to the element
                //basically styles the message.
            .addClass(`msg ${cssClass}`);
    }
    
    // Define a function to handle the submission of unique and valid words 
    async handleSubmit(formSubmitEvent) {
        //Prevents the default behavior of the form submission event; ensuring that the form is not submitted and the page reload does not occur.
        formSubmitEvent.preventDefault();
        // Select the element with the class "word" within the current instance of the board element.
            //asssigns a Jquery object associated with the element to the variable "$word"
        const $word = $(".word", this.board);
        // Assign the value of the word input field represented by "$word" using jQuery's val method.
        let word = $word.val();
        // Checks if the word input field is not empty or falsy,such as null or undefined or if its just an empty string
            // If it is empty or falsy, immediately return; to prevent the page from reloading
        if (!word) return;
        // checks if the words set contains the "word" that was submitted.
            // "has()" method of a set object checks if the word is already in the set;
                // this corrosponds to whether the word was previously submitted            
        if (this.words.has(word)) {
            // Call the statusMessage function to indicate word is already submitted using template literal syntax, and the CSS class "error" 
            this.statusMessage(`${word} exists`, "error")
            // If the word is already in the set, return the statusMessage function to indicate word is already submitted and prevent further execution of the code block
            return;
        }

        // Check validity of the server response
            // Sends async HTTP GET request to "check-word" endpoint via AXIOS library
            // The request contains a query parameter "word" with the value of the variable "word" 
        const resp = await axios.get("/check-word", { params: { word: word } });
        /* This code block handles the response from the server after checking if the submitted word is valid. It displays appropriate error messages for invalid words or words not present on the board, and updates the score and displays the word for valid words. Lastly, it clears the input field and sets the focus back to it to prepare for the next word entry.*/

        // Check if the "result" property of the server response data is equal to the string "not-word" 
        if (resp.data.result === "not-word") {
            // if the above condition is true, this indicates that the word is not a valid word on the server, and displays a message using template literal syntax, and the CSS class "error" 
            this.statusMessage(`${word} is not a valid English word`, "error");
        // Checks if the "result" property of the response data is equal to the string "not-on-board" 
        } else if (resp.data.result === "not-on-board") {
            //if the above condition is true, this indicates that the word is not a valid word on the server and displays the error message using template literal syntax, and the CSS class "error" 
            this.statusMessage(`${word} is not a valid word on this board`, "error");
        // If none of the above conditions are true, this indicates that the word is a valid word on the server and the code block below is executed to display the words in the UI, to update the displayed score in the UI, to add the words to the "words" set to keep track of the valid words found, and adds the CSS class "acceptable" to style the message.
        } else {
        this.displayWord(word);
        this.score += word.length;
        this.displayScore();
        this.words.add(word);
        this.statusMessage(`Word added: ${word}`, "acceptable");
        }
        // CLear the input field represented by "$word" using jQuery's val method and setting its value to an empty string, and then hides it from the UI (DOM).
        $word.val("").focus();
    }

    // Define displayTimer method that displays the current game timer. 
    displayTimer() {
        // The method selects the element with the class "timer" that is part of game board element, and sets the text property to the value of "this.secs" to represent the current game length in seconds (ie; time remaining).
        $(".timer", this.board).text(this.secs);
    }

    
    async tick() {
        /* Tick function that updates the timer and checks if game has ended. */

        // decrements the time property "this.secs" by 1
        this.secs -= 1;
        // calls the displayTimer method to update and display the timer
        this.displayTimer();
        // if "this.secs" is equal to 0, the game has run out of time and ended, and the interval timer is cleared using clearInterval(this.timer) to stop further execution of the tick function
        if (this.secs === 0) {
            clearInterval(this.timer);
            // It awaits the scoreGame method to update and display the score of the player
            await this.scoreGame();
        }
      }
    
  
    async scoreGame() {
        /* scoreGame` is a method of the `BoggleGame` class that hides the input elements for submitting words, sends the current score to the server, and displays corresponding status messages based on whether a new record was achieved and the final score of the game. It first hides the element with class "add-word" in the game board. Then, it sends a POST request to the "/post-score" endpoint via the AXIOS library. If the isNewRecord property of the server response data is true, indicating that the current score is a new record, it displays a message indicating the current score is a new record. If the isNewRecord property is false, it displays a message using the `statusMessage` method indicating the final score of the game. */

        // Hides the element with class "add-word" in the game board. 
        $(".add-word", this.board).hide();
        // Sends a POST rewuest to "/post-score" endpoint via AXIOS library
        const resp = await axios.post("/post-score", { score: this.score });
        // Checks if the isNewRecord property of the server response data is true; meaning that the current score is a new record.
        if (resp.data.isNewRecord) {
            // If the above condition is true, it displays a message indicating the current score is a new record, 
            this.statusMessage(`New record: ${this.score}`, "acceptable");
            // If the above condition is false, it displays a message using this.statusMessage method indicating the final score of the game.
                //It concatinates the string "Final score" with the value of "this.score" in a template literal syntax.
        } else {
          this.statusMessage(`Final score: ${this.score}`, "acceptable");
        }
    } 
    
    async endGame() {
        // Getting the score from the server
        const response = await axios.post("/post-score", { score });
        
        // If a new record was made
        if (response.data.isNewRecord) {
        $("#record-msg").show();
        }
        else {
        $("#record-msg").hide();
        }
    }
       
}



       
    
    
