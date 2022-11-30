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
        first_name = payload.first_name
        return self.test_db_query_firstname(first_name)

    def test_db_query_firstname(self, firstname):
        # import pdb; pdb.set_trace()
        author_query = db_session.query(Author).filter(Author.last_name == firstname)
        for author in author_query:
            print(author)

    def test_db(self):
        output = []
        authors = Author.query.all()
        for author in authors:
            model = {   "first_name": author.first_name,
                        "last_name": author.last_name,
                        "email": author.email,
                        "birthdate": author.birthdate,
                        "added": author.added
                    }
            output.append(model)
        # import pdb; pdb.set_trace()
        return json.dumps(output, indent=4, sort_keys=True, default=str)

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



    

   