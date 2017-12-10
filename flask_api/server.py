from flask import Flask, send_from_directory, session, request
from flask_restful import Resource, Api
from Handler import ServerHandler
from Secret import SecretKey
import requests

server_handler = ServerHandler()
app = Flask(__name__)
secret = SecretKey()
app.secret_key = secret.random_key()
api = Api(app)

class Init(Resource):
    def post(self):
    	print "Init Post Accepted"
        session.clear()
        json_data = request.get_json()
    	print json_data
        if json_data is not None:
            sec_data = {
                "secret": "6LdOMAUTAAAAAG_67lKcGHa9rlaiI6mrHczQY3hB",
                "response": json_data["g-recaptcha-response"]
            }
            r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=sec_data)
            print r.json()
	    if r.json()["success"]:
                session['uid'] = secret.random_uid()
                print 'user init: ' + session['uid']
                category = "normal"
                if int(json_data["category"]) == 0:
                    category = "normal"
                elif int(json_data["category"]) == 1:
                    category = "vegetarian"
                elif int(json_data["category"]) == 2:
                    category = "vegan"
                elif int(json_data["category"]) == 3:
                    category = "kosher"
                elif int(json_data["category"]) == 4:
                    category = "halal"
                server_handler.user_register(session['uid'], category, json_data["goals"])

                return {"success": True}
            else:
                return {"success": False}

class Update(Resource):
    def post(self):
        json_data = request.get_json()
        print json_data
        if json_data is None:
            json_data = []
        else:
            json_data = json_data['choice']
            
        if 'uid' in session and server_handler.user_verify(session['uid']):
            back_array = server_handler.phase_i(session['uid'], json_data)
            if len(back_array) > 0:
                toReturn = {'mode': 'training'}
                toReturn['urls'] = back_array
            else:
                test_array = server_handler.request_ranking(session['uid'], json_data)
                toReturn = {'mode': 'testing'}
                toReturn['urls'] = test_array
            return toReturn

class Result(Resource):
    def post(self):
        json_data = request.get_json()
        server_handler.write_to_disk(session['uid'], json_data)

api.add_resource(Init, '/init')
api.add_resource(Update, '/update')
api.add_resource(Result, '/result')
#static
@app.route('/')
def root():
    return send_from_directory('../public', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    print 'static: ' + path
    return send_from_directory('../public', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)
