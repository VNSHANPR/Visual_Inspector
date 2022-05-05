from typing import Optional

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware


from firebase_admin import credentials, initialize_app, storage
import urllib
from urllib.request import urlopen
import urllib.request
import os
import subprocess
from collections import defaultdict 
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.out_resp={}
cred = credentials.Certificate("servicekey.json")
initialize_app(cred, {'storageBucket': 'emobility-cd20b.appspot.com'})
bucket = storage.bucket()

@app.get("/sap_visualinspect_count/")
def get_last_object_count():
    b=[app.out_resp]
    response = {"value": b}
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.post("/sap_visualinspect_detect/")
async def object_detect_count(request: Request):
    received_image=[]
    received_image.append(await request.json())
    url=received_image[0]['url']
    out_reg=[]
    a=defaultdict(int)
    out_split=[]
    out=''
    out_string=''
    try:
        urllib.request.urlretrieve(url, "test1.jpg")
    except:
        return {"Error": "Invalid URL"}
    try:
        output=subprocess.check_output("cd darknet/build/darknet/x64 && ./darknet detector test data/obj.data yolo-obj.cfg yolo-obj_2000.weights /code/test1.jpg", shell=True)
        subprocess.check_output("cp darknet/build/darknet/x64/predictions.jpg .",shell=True)
        output_string= output.decode('UTF-8')
        out=output_string.replace("\n",":")
        out_split=out.split(":")
        for i in range(len(out_split)):
            out_reg.append(re.sub(r'[^a-zA-Z]', '', out_split[i]))
        for i in out_reg[15:]:
            a[i]+=1
        a.pop('')
    except: 
        return {"Error": "Nothing Detected"}
    if len((a))==0:
        response = {"Error": "Sorry, Not able to Detect"}
        app.out_resp={}
        return response
    else:
        fileName='predictions.jpg'
        global cred
        global bucket

        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)
        app.out_resp=a
        response = {"Prediction": a}
        #response.headers.add('Access-Control-Allow-Origin', '*')
        return response