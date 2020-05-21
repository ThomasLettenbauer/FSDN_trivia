import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test GET all categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # Test GET all questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['page'], 1)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] >= 0)

    # Test GET questions for one category
    def test_get_questions_for_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'Science')
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] >= 0)

    # Test delete question
    def test_delete_question(self):

        question = Question(question='Frage',
                            answer='Antwort',
                            category=1,
                            difficulty=1)
        question.insert()

        res = self.client().delete('/questions/' + str(question.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test delete nonexistent question
    def test_delete_nonexistent_question(self):

        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test POST a question / insert
    def test_post_questions_insert(self):

        body = {
            'question': 'Frage',
            'answer': 'Antwort',
            'category': 1,
            'difficulty': 1
        }

        res = self.client().post('/questions', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    # Test POST a question / insert
    def test_post_questions_insert_missing_values(self):

        body = {
            'question': 'Frage',
        }

        res = self.client().post('/questions', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # Test POST a question / search
    def test_post_questions_search(self):

        body = {
            'searchTerm': 'title',
        }

        res = self.client().post('/questions', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    # Test quizzes endpoint with category
    def test_post_quizzes(self):

        body = {
            'previous_questions': [],
            'quiz_category': {'type': "Science", 'id': "1"}
        }

        res = self.client().post('/quizzes', data=json.dumps(body), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
