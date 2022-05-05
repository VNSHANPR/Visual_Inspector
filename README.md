# Visual_Inspector
# Yolo v4 Custom Object detection & count using Fast API in a docker imager (Kyma Runtime)

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

   
 
