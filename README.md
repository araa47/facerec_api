### Updates have been made and the API is currently not compatible with the previous specs, please read throught this readme again to use the latest version of the API

# Face Recognition API BETA

##### This project is a simple face recognition api coded in python. The project uses an sqlite3 database to store the images. 


## Instructions to Use the API 


##### This API currently only supports 2 different Post Requests. Both requests are described in detail below OR check out the POSTMAN doucmentaton over here for a more detialed explanation + sample code: https://documenter.getpostman.com/view/2317617/facerec/6fU36xE

### Register Face

This is the post request to be used in order to register a new face with the corresponding filename.
You will need to direct your request to the following url:
```
http://127.0.0.1:5000/register_face/<filename>
```
filename should be replaced with the name of the file you have uploaded. An example could be the following, please remember to also add the extension of the file:
```
http://127.0.0.1:5000/register_face/obama.jpg
```

The post request also needs to contain the image itself. This can be done using the form-data format where the key is the following string "image", and the Value is the image file itself. 

#### Example Postman Request and Response
![Alt text](Facrec_register.png?raw=true "Example Postman Request and Response:")


### Find Match:

This is the post request to be used in order to find matches. You will need to use the following url:
```
http://127.0.0.1:5000/scan_for_match/<filename>/<page>

```
filename should be replaced with the name of the file you want to find matches from. Page should be replaced by an integer value. 1 is for page 1 results. 2 is for page 2 results and so on. 


```
http://127.0.0.1:5000/scan_for_match/obama.png/1
```

The post request also needs to contain the image itself. This can be done using the form-data format where the key is the following string "image", and the Value is the image file itself.

#### Example Postman Request and Response (OUTDATED , (tolerance has been changed to page number), will be updated soon)
![Alt text](Facerec_match.png?raw=true "Example Postman Request and Response:")


## Instructions to Host the API 

##### Please follow this only if you want to create your own database and host the api on your own server , if you want to use my API. You will need to make sure you have opencv installed on your computer 

1) git clone https://github.com/araa47/facerec_api

2) Make sure you have python installed, and also install virtualenv by typing in 

```
sudo pip install virtualenv
```
3) Create a new virutalenv 
```
virtualenv facerec_api
```
4) Activate the virutalenv
```
source facrec_api/bin/activate 
```
5) cd into the project
```
cd facerec_api
```
6) Install requirements to virtualenv 
```
pip install -r requirements.txt
```
7) Now You need to set up the database. The simplest way would be to comment the lines 

```
if __name__ == '__main__':
	app.run(debug=True)
```

and run the function initialize(). 

8) Now that you have the table created, you are ready to host the API. Simply undo the previous step and remove the call to the initialize function. In order to run the flask API, simply type:
```
python face_api.py
```

9) This should automatically host the API on localhost and you can continue to the next part to start testing 