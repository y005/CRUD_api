from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity
)
import time,sqlite3,bcrypt

con = sqlite3.connect("file::memory:?cache=shared", uri=True,check_same_thread=False)
cur = con.cursor()
app = Flask(__name__)

app.config.update(
        DEBUG = True,
        JWT_SECRET_KEY = "pizza",
        JWT_ACCESS_TOKEN_EXPIRES = 60*30,
        JWT_REFRESH_TOKEN_EXPIRES = 60*60*24*14
    )
jwt = JWTManager(app)

@app.route('/user/register', methods = ['POST'])
def userRegister():
    req = request.get_json()

    sql = "SELECT * FROM accounts WHERE id = ?"
    val = (req["id"],)
    cur.execute(sql,val)
    result = cur.fetchall()

    if len(result) > 0 :
        res = {"error" : "duplicate email already in db"}

    else:
        sql = "INSERT INTO accounts(id,pwd) VALUES (?,?)"
        password = req["pwd"]
        db_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        val = (req["id"],db_pwd,)
        cur.execute(sql,val)
        con.commit()
        res = {
            "id" : req["id"],
            "register date" : time.strftime('%Y-%m-%d', time.localtime(time.time()))
        }
    return jsonify(res), 200

@app.route('/user/login', methods = ['POST'])
def userLogin():
    req = request.get_json()
    try_pwd = req["pwd"]

    sql = "SELECT pwd FROM accounts WHERE id = ?"
    val = (req["id"],)
    cur.execute(sql,val)
    result = cur.fetchall()

    if len(result) > 0 :
        for tmp in result:
            real_pwd = tmp[0]
            if bcrypt.checkpw(try_pwd.encode('utf-8'), real_pwd):
                access_token = create_access_token(identity=req["id"])
                refresh_token = create_refresh_token(identity=req["id"])
                res = {
                    "access" : access_token,
                    "refresh" : refresh_token
                }
            else:
                res = {"error" : "pwd does not match"}
    else:
        res = {"error" : "email does not exist"}
    return jsonify(res), 200

@app.route('/token/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def userRefresh():
    id = get_jwt_identity()
    access_token = create_access_token(identity=id)
    res = {
        "access" : access_token
    }
    return jsonify(res), 200

@app.route('/post/viewList', methods = ['GET'])
def viewList():
    page = request.args.get('page',0,type=str)
    per_page = request.args.get('per_page',5,type=str)

    sql = "SELECT * FROM posts LIMIT ? OFFSET ?"
    val = (per_page, page,)
    cur.execute(sql,val)
    result = cur.fetchall()

    res = {
        "page": page,
        "per_page": per_page
    }

    for tmp in result:
        res.update({
            "id": tmp[0],
            "title":tmp[1],
            "content":tmp[2],
            "created time":tmp[3],
            "updated time":tmp[4]
        })

    return jsonify(res),200

@app.route('/post/view', methods = ['GET'])
def view():
    num = request.args.get('num',0,type=str)

    sql = "SELECT * FROM posts LIMIT 1 OFFSET ?"
    val = (num,)
    cur.execute(sql,val)
    result = cur.fetchall()

    res = {
        "num": num
    }

    for tmp in result:
        res.update({
            "id": tmp[0],
            "title":tmp[1],
            "content":tmp[2],
            "created time":tmp[3],
            "updated time":tmp[4]
        })
    return jsonify(res),200

@app.route('/post/create', methods = ['POST'])
@jwt_required()
def createPost():
    id = get_jwt_identity()
    req = request.get_json()
    title = req["title"]
    content = req["content"]
    if (len(title) == 0) and (len(content) == 0):
        return jsonify({"error": "write both title and content"}),200

    sql = "SELECT * FROM accounts WHERE id = ?"
    val = (id,)
    cur.execute(sql,val)
    result = cur.fetchall()

    if len(result) > 0:
        created_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        for tmp in result:
            id = tmp[0]
        sql = "INSERT INTO posts(id,title,content,created_time,edited_time) VALUES (?,?,?,?,?)"
        val = (id,title,content,created_time,created_time,)
        cur.execute(sql,val)
        con.commit()
        res = {
            "id": id,
            "title": title,
            "content": content,
            "created_time": created_time,
            "edited_time": created_time
        }
    else:
        res = {"error" : "can't post"}

    return jsonify(res),200

@app.route('/post/update/<str:num>', methods = ['PATCH'])
@jwt_required()
def updatePost(num):
    req = request.get_json()
    title = req["title"]
    content = req["content"]
    if (len(title) == 0) and (len(content) == 0):
        return jsonify({"error": "write both title and content"}),200

    id = get_jwt_identity()
    sql = "SELECT id,created_time FROM posts LIMIT 1 OFFSET ?"
    val = (num,)
    cur.execute(sql,val)
    result = cur.fetchall()

    for tmp in result:
        if tmp[0] == id:
            edited_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            sql = "update posts set title = ?, content = ?, edited_time = ? LIMIT 1 OFFSET ?"
            val = (title,content,edited_time,num,)
            cur.execute(sql,val)
            con.commit()
            res = {
                "id": id,
                "title": title,
                "content": content,
                "created_time": tmp[1],
                "edited_time": edited_time
            }
            return jsonify(res)
        else:
            return jsonify({"error": "can't update other user post"}),200

@app.route('/post/delete/<str:num>', methods = ['DELETE'])
@jwt_required()
def deletePost(num):
    id = get_jwt_identity()
    sql = "SELECT id FROM posts LIMIT 1 OFFSET ?"
    val = (num,)
    cur.execute(sql,val)
    result = cur.fetchall()

    for tmp in result:
        if tmp[0] == id:
            sql = "delete from posts LIMIT 1 OFFSET ?"
            val = (num,)
            cur.execute(sql,val)
            con.commit()
            res = {
                "success": "delete post"
            }
            return jsonify(res)
        else:
            return jsonify({"error": "can't delete other user post"}),200

def setting_db():
    cur.execute("CREATE TABLE IF NOT EXISTS posts(id text,title text NOT NULL,content text NOT NULL,created_time text,edited_time text,FOREIGN KEY (id) REFERENCES accounts(id))")
    cur.execute("CREATE TABLE IF NOT EXISTS accounts(id text PRIMARY KEY,pwd text NOT NULL)")
    con.commit()

if __name__ == "__main__":
    setting_db()
    app.run()
