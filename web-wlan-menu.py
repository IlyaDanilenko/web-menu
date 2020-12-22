#!/usr/bin/python3

from rosnode import get_node_names
from rosservice import get_service_list, get_service_type, get_service_node
from rostopic import get_topic_list
import os
from time import sleep
import subprocess
from flask import Flask,send_file,render_template,jsonify,request

app = Flask(__name__)
roscore = None
launch = None

@app.route('/')
def index():
    global hostname
    return render_template('index.html',host=hostname)

@app.route('/com',methods=['POST'])
def com():
    global roscore
    c = int(request.form['com'])
    if(c==1):
        roscore = subprocess.Popen("roscore", stdout=subprocess.DEVNULL)
        return jsonify(status=1)
    else:
        if roscore != None:
            roscore.terminate()
            roscore = None
        return jsonify(status=0)
    return jsonify(status=-1)
    
@app.route('/launch_start',methods=['POST'])
def launch_start():
    global launch
    launch = subprocess.Popen(["roslaunch","gs_core","pioneer.launch"], stdout=subprocess.DEVNULL)
    return jsonify(status=1)

@app.route('/launch_stop',methods=['POST'])
def launch_stop():
    global launch
    if launch == None:
        return jsonify(status=0)
    else:
        launch.terminate()
        launch = None
        return jsonify(status=1)

@app.route('/launch_status')
def launch_status():
    global launch
    if launch == None:
        return jsonify(status=0)
    else:
        return jsonify(status=1)

@app.route('/core')
def core():
    try:
        get_node_names()
        return jsonify(status=1)
    except:
        return jsonify(status=0)

@app.route('/node')
def get_nodes():
    try:
        nodes = get_node_names()
        return jsonify(status=0,list=nodes)
    except:
        return jsonify(status=-1,list=[])

@app.route('/service')
def get_services():
    try:
        services = get_service_list()
        m = []
        n = []
        for i in services:
            m.append(get_service_type(i))
            n.append(get_service_node(i))
        return jsonify(status=0,list=services,type=m,node=n)
    except:
        return jsonify(status=-1,list=[],type=[],node=[])

@app.route('/topic')
def get_topic():
    try:
        topics = get_topic_list()
        t = []
        m = []
        n = []
        for i in topics[0]:
            t.append(i[0])
            m.append(i[1])
            k = ""
            for j in i[2]:
                k += j + ","
            k = k[0:len(k)-1]
            n.append(k)
        return jsonify(status=0,list=t,type=m,node=n)
    except:
        return jsonify(status=-1,list=[],type=[],node=[])

try:
    sleep(10)
    hostname = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
    app.run(host=hostname,port=9090)
except:
    pass
