import sqlite3
import cv2 
import face_recognition 
import json 
from numpy import array 
import os 
import pickle 
import time


from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

# Only run this on the first run incase you want to creat a new table 
def initialize():

	# Reference name of sqlite3 database 
	connection = sqlite3.connect("tide_av_faces.db")

	# Create a cursor object 
	cursor = connection.cursor()

	try:
		# Delete table if exists
		cursor.execute("""DROP TABLE faces;""")

	except Exception as e:
		# This just handles the table not existing 
		print "Exception Occured: " + e + " <You can mostly ignore this exception> " 


	# Create a table sql comand string 
	sql_command = """ CREATE TABLE faces (id INTEGER PRIMARY KEY, filename TEXT, face_encoding BLOB);"""

	try: 
		# Create the table
		cursor.execute(sql_command)
	except Exception as e:
		# This handles the table already existing 
		print  "Exception Occured: " + e + " <You can mostly ignore this exception> " 
	
	# close the connection 
	connection.close()


# Function to get a face encoding array from an image: inpupt: filename, output: face_encoding array
def face_encode(filename):
	# read the image
	image = cv2.imread(filename)	
	# scan the image for faces
	face_locations = face_recognition.face_locations(image)
	# get face encoding from the face locations 
	face_encodings = face_recognition.face_encodings(image, face_locations, num_jitters=1)
	# return the face encoding 
	return face_encodings

# Reads the db and returns the face table name and corresponding face array 
def read_all_db():
	## Reference name of sqlite3 database 
	connection = sqlite3.connect("tide_av_faces.db")
	# Create a cursor object 
	cursor = connection.cursor()
	sql_command = """ SELECT * FROM faces """
	cursor.execute(sql_command)
	result = cursor.fetchall()
	return result


# Registers faces to the database 
def register_to_db(filename):
	## Reference name of sqlite3 database 
	connection = sqlite3.connect("tide_av_faces.db")
	# Create a cursor object 
	cursor = connection.cursor()
	# get the face encoding
	face_encodings = face_encode(filename)
	# convert for easy storage on database
	face_encodings = json.dumps(str(face_encodings))

	sql_command =  """ INSERT INTO faces VALUES (NULL, \'%s\', \'%s\');"""%(filename, face_encodings,)
	cursor.execute(sql_command)
	connection.commit()
	connection.close()
	return True



def scan_for_match(filename, tolerance):

	# get users face encoding
	user_f_e = face_encode(filename)

	# now read the database 
	data = read_all_db()

	# new list for storing the match names 
	match_list = []

	# iterate through the databse
	for i in range(len(data)):
		# get the filenae as python variable
		db_filename = data[i-1][1]
		# get the face encoding as python variable
		db_encoding = eval(str(json.loads(data[i-1][2])))	

		# for each face encoding in the face_encoding array 
		for single_encoding in db_encoding:
			# check if there is a match 
			match_user = face_recognition.compare_faces(user_f_e, single_encoding, tolerance)
			
			# THis is for error handling incase there was a problem running the compare_faces 
			try:
				# if there is a match 
				if match_user[0]:
				# 	Print out the name of the match 
				#	print "Match Found: " + str(db_filename.encode('utf8'))
				# Add the match to match_list 
					match_list.append(db_filename)
			# Exceptoion handling 
			except Exception as e:
				print "Error While running compare_faces, " + str(e)
				return "Error: " + str(e) + " Please try another image"

# Print out all the matches 
	print "All Matches: " + str(match_list)
# Return the match list 
	return match_list


# This function is only used to register matches really fast without having to send api requests each time 
def main_register():
	import glob 
	# read all the filenames withitn the following folder 
	scrapename = glob.glob("image_database/*")
	# iterate through the files
	for files in scrapename:
		# print out the filename
		print files 
		# register the file to database 
		register_to_db(files)



# image here is a special type that is part of a post request (Used when recieving requests to locally store the iamge for processing)
# __TODO__ : Need to add a delete file part where the images are deleted after they are registered or used
def write_file(image, filename):
	with open(filename, 'w') as fp:
			for item in image:
				fp.write(item)


# This checks if the image format send is an allowed file extension and will fail incase the file is the wrong format
def allowed_file(filename):
	ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
	# get the extension from filename by getting conent after the .
	extension = filename.split(".")[1]
	# check if it is part of allowed_extensions 

	if extension in ALLOWED_EXTENSIONS:
		return True 
	else:
		return False 


# This is for the Restful, Post request inorder to register a face to the database
@app.route('/register_face/<filename>', methods=['POST'])
def register_command(filename):

	start_time = time.time()

	# get the imagefile
	image = request.files['image']
	# check if its correct format
	check = allowed_file(filename)

	if check == True:
		print "Pass"
		filename = "Temp/" + filename
		write_file(image, filename)
		register_sucess = register_to_db(filename)
		if register_sucess == True:
			os.remove(filename)
			print "Elapsed: " + str(time.time() - start_time)
			return jsonify({"Operation Sucess" : True})

		else:
			return jsonify({"Error": "Can't seem to decode your file" })
		
	else:
		return jsonify({"Error": "Please enter a valid file type" })


@app.route('/scan_for_match/<filename>/<float:tolerance>', methods=['POST'])
def scan_matches(filename, tolerance):
	start_time = time.time()
	# get the imagefile
	image = request.files['image']
	tolerance = float(tolerance)
	# check if its correct format
	check = allowed_file(filename)

	if check == True:
		print "Pass"
		filename = "Temp/" + filename
		write_file(image, filename)
		match_list = scan_for_match(filename, tolerance)
		if len(match_list) > 0:
			print "Elapsed: " + str(time.time() - start_time)
			return jsonify({"Operation Sucess" : True, 
							"Match Results" : match_list})

		else:
			return 	jsonify({"Operation Sucess" : True,
							"Match Results": None})

	else:
		return jsonify({"Error": "Please enter a valid file type" })


def deciding_algo():
	# try initially with 0.5 
	print "Still in progress"
	
	


if __name__ == '__main__':
	app.run(debug=True)




#print scan_for_match("image_scrape/img_14.jpg", 0.6)








#connection.close()