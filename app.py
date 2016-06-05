from flask import Flask
from dbhandler import DBHandler
import config


app = Flask(__name__)
dbhandler = DBHandler(config.DATABASES['default'])
db = dbhandler.initialize(app, ['user_account'])


@app.route('/test')
def test_request():
    User = dbhandler.user_account
    usr = db.session.query(User).filter_by(username='jsangilve').first()
    return usr.username

if __name__ == '__main__':
    app.run(debug=True)
