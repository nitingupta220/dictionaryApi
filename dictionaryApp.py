from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
import operator
app =  Flask(__name__)

app.config.update({
    'DEBUG' : True
})
users = [
    { 'name': 'nitin', 'password' : 'gupta' }, { 'name' : 'dhannu', 'password' : 'mayank' }
]

words = [
    { 'word' : 'exaggerate',
        'note' : 'to express something in larger manner but in reality it is not',
        'user' : 'nitin',
        'id' : 1,
        'difficulty' : 5
      },
    { 'word' : 'context',
        'note' : 'to express something ',
        'user' : 'nitin',
        'id' : 2,
        'difficulty' : 6
      },
    {
        'word' : 'something',
        'user' : 'dhannu',
        'note' : 'nothing',
        'id' : 2,
        'difficulty' : 6
    },
    {
        'word' : "happy",
        'note' : "to live happy",
        'user' : 'nitin',
        'difficulty' : 4,
        'id' : 3
    }
]

@auth.get_password
def get_password(username):
    user = [user for user in users if username == user['name']]
    if len(user) == 0:
        abort(400)
    return user[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error' : 'Unauthorized'}),401)


@app.route('/getwords', methods = ['GET'])
@auth.login_required
def get_words():
    word = [word for word in words if auth.username() == word['user']]
    user = request.args.get('user')
    if user == 'id':
        new_words = sorted(word, key=lambda k: k['id'])
    elif user == 'difficulty':
        new_words = sorted(word, key=lambda k: k['difficulty'])
    elif user == 'word':
        new_words = sorted(word, key=lambda k: k['word'])
    else:
        abort(400)
    return jsonify({'new_words':new_words})



@app.route('/user', methods = ['POST'])
def new_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = {
        'name' : request.json['name'],
        'password' : request.json['password']
    }
    users.append(user)
    return jsonify({'user':user}), 201


@app.route('/words', methods = ['POST'])
def add_word():
    if not request.json or not 'word' in request.json:
        abort(400)
    word = {
            'word' : request.json['word'],
            'note' : request.json['note'],
            'id' : words[-1]['id']+5,
            'user' : auth.username(),
            'difficulty' :request.json['difficulty']
    }
    words.append(word)
    return jsonify({'word' : word}), 201


if __name__ == '__main__':
    app.run()