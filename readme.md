# Welcome to SharedBoard!

This project is implement for as a task for MaralHost corporation.
It's a share board flask app that share tickets from authenticated users.
It uses Flask as backend framework and utilities many other packages that include in requirements.txt file. 



# Run

First run bellow command to install all required packages:

    $ pip install -r requirements.txt
It's recommended to install packages in local environments using **virtualenv** package.
   
Second make sure  **redis** is installed.

Then set your settings for this project in .flaskenv:

    export FLASK_ENV=development
    export FLASK_APP=src
    export SQLALCHEMY_DB_URI="sqlite:///boards.sqlite"
    export SECRET_KEY="This is the real secret key"
    export JWT_SECRET_KEY="This is jwt secret key"
Above values are meant only for development environments.

When your done with the above steps then you are ready to run the app. Just type bellow line in command line:

    $ flask run

Now flask app is running on port 5000 and you can send requests to it.



# API Endpoints
These are available api endpoints with their description:

	url: /api/v1/auth/register
	description: To sign up users
	method: POST
	payload: {
		"username": "amin",
		"email": "amin@example.com",
		"password": "aminpassword"
	}

	
	/api/v1/auth/login
	description: To sign in users
	method: POST
	payload: {
		"email": "amin@example.com",
		"password": "aminpassword"
	}

	
	url: /api/v1/auth/logout
	description: To sign out users
	method: DELETE
	payload: payload not required
	* requires jwt access token to be set

	
    url: /api/v1/auth/token/refresh	
	description: To refresh access token
	method: POST
	payload: payload not required
	* requires jwt refresh token to be set

	
    url: /api/v1/tickets
	description: To fetch all tickets shared on the board
	method: GET
	payload: payload not required
	* requires jwt access token to be set
	
	
    url: /api/v1/tickets
	description: To create new ticket on the board
	method: POST
	payload: {
		"body": "body of the ticket goes in here."
	}
	* requires jwt access token to be set
	
	
	/api/v1/tickets/<id>
	description: To update ticket on the board
	method: PUT
	payload: {
		"body": "body of the ticket goes in here."
	}
	* requires jwt access token to be set
