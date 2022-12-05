from flask import request, jsonify
import simplejson as json
from flaskbase.flask_model.flask_model import Author
from flaskmicro.database import db_session
from sqlalchemy import inspect


class Controller:
    """
    Controller
    """
    # def get_test_api(self):
    #     """"""
    #     test = {'test': 'test successful'}
    #     return json.dumps(test)

    def get_test_db_insert(self, payload):
        first_name = payload.first_name
        last_name = payload.last_name
        email = payload.email
        birthdate = payload.birthdate
        added = payload.added
        self.test_db_insert(first_name, last_name, email, birthdate, added)
        return "Insert successful"

    def get_test_db(self):
        return self.test_db()

    def get_test_db_query(self, payload):
        last_name = payload.last_name
        return self.test_db_query_firstname(last_name)

    def test_db_query_firstname(self, last_name):
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

    def test_db(self):
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
        # import pdb; pdb.set_trace()
        return json.dumps(response, indent=4, sort_keys=True, default=str)

        # authors = Author.query.all()
        # for author in authors:
        #     print(author)

    def test_db_insert(self, first_name, last_name, email, birthdate, added):
        u = Author(first_name, last_name, email, birthdate, added)
        db_session.add(u)
        db_session.commit()

    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}



    

   