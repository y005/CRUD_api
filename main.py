from flask import Flask, request, jsonify  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
import pandas as pd

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록

@api.route('/checkDeadline')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class checkDeadline(Resource):
    def post(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        data = pd.read_csv('deadline.csv')
        answer = data["date"][len(data)-1]
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }

        return jsonify(res)

@api.route('/checkInfo')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class checkInfo(Resource):
    def post(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        data = pd.read_csv('info.csv')
        answer = data["text"][len(data)-1]
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }

        return jsonify(res)

@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class hello(Resource):
    def post(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        answer = "안녕하세요"
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }

        return jsonify(res)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
