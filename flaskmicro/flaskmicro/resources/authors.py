from flask import request, jsonify
import simplejson as json
from flaskbase.flask_model.flask_model import Author
from flaskmicro.database import db_session
from sqlalchemy import inspect


class Controller:
    """
    Controller
    """

    def get_test_db_insert(self, payload):
        first_name = payload.first_name
        last_name = payload.last_name
        email = payload.email
        birthdate = payload.birthdate
        added = payload.added
        self.insert_add_commit(first_name, last_name, email, birthdate, added)

        model = {
            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "email": payload.email,
            "birthdate": payload.birthdate,
            "added": payload.added,
        }

        return json.dumps(model)

    def get_test_db_query(self, payload):
        last_name = payload.last_name
        return self.test_db_query_last_name(last_name)

    def test_db_query_last_name(self, last_name):
        response = []
        author_query = db_session.query(Author).filter(Author.last_name == last_name)
        for author in author_query:
            model = {   "first_name": author.first_name,
                        "last_name": author.last_name,
                        "email": author.email,
                        "birthdate": author.birthdate,
                        "added": author.added
                    }
            response.append(model)
        return json.dumps(response, indent=4, sort_keys=True, default=str)

    def get_test_db(self):
        response = []
        authors = Author.query.all()
        for author in authors:
            model = {   "first_name": author.first_name,
                        "last_name": author.last_name,
                        "email": author.email,
                        "birthdate": author.birthdate,
                        "added": author.added
                    }
            response.append(model)
        return json.dumps(response, indent=4, sort_keys=True, default=str)

    def insert_add_commit(self, first_name, last_name, email, birthdate, added):
        author = Author(first_name, last_name, email, birthdate, added)
        db_session.add(author)
        db_session.commit()




    

   