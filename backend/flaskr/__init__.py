import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {category.id: category.type
                                for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():

        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        categories = Category.query.all()
        formatted_categories = {category.id: category.type
                                for category in categories}
        current_category = Category.query.first().type

        print(current_category)

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'categories': formatted_categories,
            'current_category': current_category,
            'total_questions': len(formatted_questions),
            'page': page
        })

    @app.route('/categories/<int:id>/questions')
    def get_categoryquestions(id):
        try:
            questions = Question.query.filter(Question.category == id)
            category = Category.query.get(id)
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': category.type
            })

        except Exception:
            abort(422)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        try:
            searchterm = request.get_json().get('searchTerm')

            if searchterm:
                ''' SEARCH '''
                questions = Question.query.filter(
                    Question.question.ilike("%" + searchterm + "%"))
                formatted_questions = [question.format()
                                       for question in questions]

                return jsonify({
                    'success': True,
                    'questions': formatted_questions
                })
            else:
                ''' INSERT '''
                question = request.get_json()['question']
                answer = request.get_json()['answer']
                category = request.get_json()['category']
                difficulty = request.get_json()['difficulty']

                question = Question(question=question,
                                    answer=answer,
                                    category=category,
                                    difficulty=difficulty)

                question.insert()
                return jsonify({
                    'success': True
                })
        except Exception:
            abort(400)

    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        try:
            previous_questions = request.get_json()['previous_questions']
            quiz_category = request.get_json()['quiz_category']

            print(previous_questions)

            if quiz_category['id'] == 0:
                # All Categories
                question = Question.query \
                                   .filter(~ Question.id.in_(previous_questions)) \
                                   .order_by(func.random()).limit(1).all()[0]
                formatted_question = question.format()
            else:
                # One Category
                question = Question.query \
                                   .filter(Question.category == quiz_category['id']) \
                                   .filter(~ Question.id.in_(previous_questions)) \
                                   .order_by(func.random()).limit(1).all()[0]
                formatted_question = question.format()
            return jsonify({
                'success': True,
                'question': formatted_question
            })
        except Exception:
            abort(400)

    # Errorhandlers

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
