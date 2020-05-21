# Trivia API Documentation
## Error Handling
Errors are returned as JSON objects in the following format:

        {
	      "error": 405, 
	      "message": "Method Not Allowed", 
	      "success": false
	    }
	    
The API will return  4 error types when requests fail:
* 400: Bad Request
* 404: Resource Not Found
* 405: Method Not Allowed
* 422: Not Processable

## Endpoints
### GET /questions
* General:
	* Returns a list of categories, question objects, current category, success value and total number of questions
	* Results are paginated in groups of 10. Include a request argument *page* to choose page number, starting from 1
* Sample: 

	    curl http://127.0.0.1:5000/questions

* Response:

        {
      "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
      }, 
      "current_category": "Science", 
      "page": 1, 
      "questions": [
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
          "answer": "Muhammad Ali", 
          "category": 4, 
          "difficulty": 1, 
          "id": 9, 
          "question": "What boxer's original name is Cassius Clay?"
        }, 
      ], 
      "success": true, 
      "total_questions": 2

### GET /categories
* General:
	* Returns a list of categories and success value
* Sample: 
	
	    curl http://127.0.0.1:5000/categories

* Response:

	    {
	      "categories": {
	        "1": "Science", 
	        "2": "Art", 
	        "3": "Geography", 
	        "4": "History", 
	        "5": "Entertainment", 
	        "6": "Sports"
	      }, 
	      "success": true
	    }

### GET /categories/\<id\>/questions
* General:
	* Returns a list of question objects for category id *id*

* Sample: 
	

	    curl http://127.0.0.1:5000/categories/1/questions

* Response:
	
	    {
		      "current_category": "Science", 
		      "questions": [
		        {
		          "answer": "Alexander Fleming", 
		          "category": 1, 
		          "difficulty": 3, 
		          "id": 21, 
		          "question": "Who discovered penicillin?"
		        }, 
		        {
		          "answer": "Blood", 
		          "category": 1, 
		          "difficulty": 4, 
		          "id": 22, 
		          "question": "Hematology is a branch of medicine involving the study of what?"
		        }, 
		        {
		          "answer": "answertext", 
		          "category": 1, 
		          "difficulty": 1, 
		          "id": 61, 
		          "question": "questiontext"
		        }
		      ], 
		      "success": true, 
		      "total_questions": 3
		   }
	   
### DELETE /questions/\<id\>
* General:
	*  Deletes the question with id *id*

* Sample: 
	

	    curl -X DELETE http://127.0.0.1:5000/questions/23
* Response:

	    {
	      "deleted": 23, 
	      "success": true
	    }
	      

### POST /questions
* General:
	* Inserts a new question with values for question, answer, category and difficulty in the body
	* Returns a success value

* Sample: 

	    curl 	--header "Content-Type: application/json" --request POST \
				--data '{"question":"Frage","answer":"Antwort", "category":1, "difficulty":1}' \
				http://127.0.0.1:5000/questions
* Response:

	    {
	    	  "success": true
	    }

### POST /quizzes
* General:
	* Returns a success value and one question, excludes question ids from the array *previous_questions*
	
* Sample: 

		curl 	--header "Content-Type: application/json" \
				--request POST \
				--data '{"previous_questions":[4], "quiz_category":{"type":"Science", "id":"1"}}' 	\	
				http://127.0.0.1:5000/quizzes
* Response:

	    {
	      "question": {
	        "answer": "Tom Cruise", 
	        "category": 5, 
	        "difficulty": 4, 
	        "id": 4, 
	        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
	      }, 
	      "success": true
	    }