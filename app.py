from flask import Flask,jsonify,request,session
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash
from flask_pymongo import PyMongo
import bcrypt






app=Flask(__name__)
app.config['MONGO_DBNAME'] = 'blockchain'
app.config['MONGO_URI'] = '<MONGODB DB LINK>'

mongo=PyMongo(app)

EMAIL=[]
BITCOIN=[]


#route helps user to register 
@app.route("/register",methods=["POST"])
def get_register():
    _json=request.json
    name=_json["name"]
    email=_json["email"]
    password=_json["password"]
   # _bitcoin=_json["bitcoin"]
    users = mongo.db.collection
    existing_user = users.find_one({'name' :name})
    if existing_user is not None: 
           return {'status':'This username already exsist!'}
    
    if name and email and password and request.method=='POST':

        hashed_password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({"name":name,"email":email,"password":hashed_password})
        user=users.find_one({'email':email})
        iD=user["_id"]
        name=user["name"]
        email=user["email"]
        password=user["password"]
        
        resp={
            "id":iD,
            "name":name,
            "email":email,
            "password":password
        }
        EMAIL.append(email)
        print('Email',EMAIL)
        #result =serialize(resp)
        data=json.loads(json_util.dumps(resp))

        return data
    else:
        return {'status':'failed'}
@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message'  :'Not Found'+request.url
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp

#route will ask user to login every time they open the app
@app.route('/login',methods=['GET','POST'])
def get_login():

    if request.method == 'POST':
        json=request.json
        Email=json["email"]
        pwd=json["password"]
        users = mongo.db.collection
        
        existing_user = users.find_one({'email' : Email})
        
        if existing_user is None:
                return {'status':'Please register before logging in!'}
        else:
            if bcrypt.hashpw(pwd.encode('utf-8'), existing_user['password']) == existing_user['password']:
                    resp={
                       "email":Email,
                       "password":pwd
                        }
                    return {'status':'logged in'}
                #redirect to investment tab
          
        return {'status':'Username/Password is invalid'}
   
 

#route gets the value of bitcoin that the user wants to invest
@app.route('/investment',methods=['GET','POST'])
def get_investment():
# input:the bitcoin that user wants to invest

    json=request.json
    bcoin=json["Bcoin"]
    BITCOIN.append(bcoin)
    print(EMAIL)
    val=EMAIL[len(EMAIL)-1]
    users = mongo.db.collection
    user=users.find_one({'email':val})
    
    users.update_one({"_id": user["_id"]}, {"$set": {"Bcoin":bcoin}})

    return {"Bcoin":user["Bcoin"]}

#route provides users the potential companies where they can invest   
@app.route('/detail',methods=['GET'])
def get_detail():
    import companydetails

    name=[companydetails.name]
    price=[companydetails.oen]
    ret=[companydetails.ret]
    return {"name":name,"openingPrice":price,"return%":ret}

#allow users to buy the share of their desired company this transaction is
#done using blockchain
@app.route('/buy_shares',methods=['GET','POST'])
def buy_shares():
    
    # input: invested amount in bitcoin
    global amt
    import chain
    json=request.json
    amt=json["Amount"]
    s=chain.s
    return {'status':'Transaction successfull'}

#if the users wants to sell their shares
@app.route('/sell',methods=['GET'])
def sell():
    #input:bitcoin value
    invested_amt = BITCOIN[len(BITCOIN)-1]
    invested_amt=int(invested_amt)
    sell = invested_amt*0.02
    return {"value":sell}
    
        
if __name__ == "__main__":
    app.run(debug=False)  
