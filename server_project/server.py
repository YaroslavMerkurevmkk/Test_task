from flask_restful import Api
from flask import Flask
from flask_restful import abort, Resource
from flask import jsonify
from requests import get

from flask_restful import reqparse

from flask_sqlalchemy import SQLAlchemy

cnx = {
    'connector': 'mysql+pymysql',
    'user': 'flask',
    'password': 'password',
    'host': 'mysql',
    'database': 'flask'
}

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "sefsef8&fdsejJgbyGYhGGf09/d,a"
app.config['SQLALCHEMY_DATABASE_URI'] = '{connector}://{user}:{password}@{host}/{database}'.format(**cnx)

db = SQLAlchemy(app=app)


class Quiz(db.Model):
    __tablename__ = 'flask'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    id_question = db.Column(db.Integer)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    created_date = db.Column(db.Text)


with app.app_context():
    db.create_all()


def add_question(id_question: int, question: str, answer: str, created_date: str) -> bool:
    if not Quiz.query.filter_by(question=question).first():
        quiz_question: Quiz
        quiz_question = Quiz(id_question=id_question, question=question, answer=answer, created_date=created_date)
        with app.app_context():
            db.session.add(quiz_question)
            db.session.commit()
        return True
    return False


parser = reqparse.RequestParser()
parser.add_argument("questions_num", required=True, type=int)
parser.add_argument("token", required=True, type=str)


def check_token(token: str) -> None:
    server_token = 'efsfsefsefw453srgrgrg'
    if token != server_token:
        abort(404)


class QuizResource(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            questions_num = args['questions_num']
            token = args["token"]
            check_token(token=token)
            url = "https://jservice.io/api/random?count=1"
            success_response = 0
            while success_response != questions_num:
                response = get(url=url)
                if response.ok:
                    data = response.json()
                    id_question = data[0]["id"]
                    question = data[0]["question"]
                    answer = data[0]["answer"]
                    created_date = data[0]["created_at"]
                    if add_question(id_question=id_question,
                                    question=question,
                                    answer=answer,
                                    created_date=created_date):
                        success_response += 1
            return jsonify(result="success", question=question)
        except Exception as e:
            return jsonify(result=e)


def main():
    api.add_resource(QuizResource, "/api/quiz")
    app.run(host='0.0.0.0', debug=False)


if __name__ == "__main__":
    main()
