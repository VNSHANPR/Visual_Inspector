# Visual_Inspector
# Yolo v4 Tiny on CPU Custom Object detection & count using Fast API in a docker imager (Kyma Runtime)

Watch a Short Video on Youtube : [Visual Inspector](https://www.youtube.com/watch?v=IdRq3stH-4Al-Y "Visual Inspector")

Few images of the project deployed in AppGyver ( low code mobile App - essentially the deployed API being called inside the App) :

Darknet code & credit : https://github.com/AlexeyAB/darknet

<img src="https://user-images.githubusercontent.com/41034062/166865652-1c8900cc-8e6d-43fd-b43c-2c5916739d65.png" alt="drawing" style="width:290px;"/>--------------------------------------------<img src="https://user-images.githubusercontent.com/41034062/166865486-5fb5bcd5-20a3-482a-8b35-b180d207766b.png" alt="drawing" style="width:315px;"/>

Project provides a basic outline on developing a custom object detection project using Yolo V4 and exposing a reusable API (python FastAPI) which takes the Image URL (Stored in Object store) and then runs a detection on it , finally outputting the new image with bounding boxes and a count of the detected Custom objects.The output image with bounded boxes is saved as prediction.jpg in google firebase store once the POST call returns from the API, this image is used as the output image in the mobile App showing the detected objects. (Image is overwritten after each post call)

Key Points : 

    - Train a custom detection model using Yolo V4 as detailed here (https://github.com/AlexeyAB/darknet) on Google Colab. 
    - Save your best performing model weights file from the Google colab session (under /darknet/build/x64/backup) and upload to the app/darknet/build/x64 folder (yolo-obj_2000.weights in our example)
    - Run a basic ubuntu container and build ('make' utility on linux) darknet , we will use a compiled darknet folder in our docker image. (in this repo this is already provided under apps)
    

We are using Fast API to create a "GET" and "POST" route in main.py
 - /sap_visualinspect_count/ - Returns the count of the last object detection performed
 - /sap_visualinspect_detect/ - Takes in an image URL , uses the image to perform detection applying custom trained weights, returns the number of objects detected as nested json and also updates prediction.jpg file in Google Firebase object store which is used in the mobile app to show the result of the current detection with bounded boxes. (function is using also an image name which is not utilized)

 # How to run the Project using Docker ?

 - Clone the repo
 - Create your firebase storage account and generate a servicekey.json 
 - update your storage bucket name in line 29 of app/main.py
 - Build docker image from the base folder :
   ``` docker build . ```
 - Tag your docker image :
    ``` docker tag 590c5b8bc288 fastapi_visualinspect ```
 - Run your image :
   ``` docker run -d -p 8090:8090 fastapi_visualinspect:v3 ```


  # Run a detection 

   Upload few images in your firebase google storage, get the URL including the token, perform a POST request using below sample json on POSTMAN : 

   ```json
           {
          "filename": "doesnotmatter",
          "url": "https://firebasestorage.googleapis.com/v0/b/emobility-cd20b.appspot.com/o/64.jpg?alt=media&token=44324805-02a5-4a78-adcb-d09ce25059db"
        }

   ```
   header: 
   Content-Type : application/json
   
   ![image](https://user-images.githubusercontent.com/41034062/166861007-ca0251f0-7044-4ea8-ba91-45df0a74c127.png)

   the POST call returns the detected object "box" and the count "8" in this case.
   
   Here is the preview of the input Image & the output saved as predictions.jpg in Google Firebase Account : 
   
   <img src="https://user-images.githubusercontent.com/41034062/166861074-e0438050-5538-48d8-acfb-0374a6aac8a9.png" alt="drawing" style="width:500px;"/> <img src="https://user-images.githubusercontent.com/41034062/166861165-f6951eb2-6230-442e-8dd9-4b08e7c84933.png" alt="drawing" style="width:500px;"/>

   
   
   



