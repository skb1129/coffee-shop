# Coffee Shop

Coffee Shop is a full stack project, part of Udacity's Full Stack Nanodegree. The server for this application is build
in Python using Flask. The client app is build using Ionic and Angular.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

You need the following applications to run the server app:
1. Python 3.7
2. Pipenv (_Optional_)

You need the following applications to run the client app:
1. Node 11+
2. NPM

### Installing

It is preferred if you run this in a virtual environment for python. If you are using `pipenv`, virtual environment
would be taken care of by `pipenv`. Instructions for setting up a virtual environment for your platform can be found in
the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Installing the server dependencies:
1. Change directory to `./backend`.
2. Install the requirements:
```bash
pipenv install
```
or if you are not using `pipenv`:
```bash
pip install requirements.txt
```

Installing the client dependencies:
1. Change directory to `./frontend`.
2. Install the requirements:
```bash
npm i
```

## Running the application

Starting the server:
1. Change directory to `./backend`.
2. Run the following commands:
```bash
export FLASK_APP=src/api.py
flask run
```
3. The application will be serve on **http://localhost:5000**

Starting the client:
1. Change directory to `./frontend`.
2. Run the following script:
```bash
npm run start
```
3. The application will be serve on **http://localhost:4200**

Now, go to **http://localhost:4200** to view the Coffee Shop app.

## Test Users:

The application uses Auth0 for authenticating users. I have created 2 test users with different roles to test the
application.

**Barista**
Username => `barista@coffee-shop.com`
Password => `Barista@coffee-shop`

**Manager**
Username => `manager@coffee-shop.com`
Password => `Manager@coffee-shop`

## Built With

* [Flask](http://flask.pocoo.org/) - The python server micro framework
* [Angular](https://angular.io/) - The front end MVC framework

## Authors

**Surya Kant Bansal** - *Developer* - [skb1129](https://github.com/skb1129)

## Acknowledgments

* [Udacity](https://www.udacity.com/)
* [Auth0](https://auth0.com/)
