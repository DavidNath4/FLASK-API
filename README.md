# Movie API Documentation
![flaskAPI drawio](https://github.com/DavidNath4/FLASK-API/assets/73566173/5a9de932-a840-47be-8eff-ef87de3964fd)

## Getting Started

1. Create a new virtual environment:

    ```bash
    python -m venv env
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```
3. Create and set .env contains
    ```
    FLASK_APP = app.py
    FLASk_ENV = development
    FLASK_DEBUG = True
    FLASK_RUN_HOST = localhost
    FLASK_RUN_PORT = 5030
    SECRET_KEY = ''
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    JWT_SECRET_KEY = ''
    ```

4. Create mysql database
    ```
    CREATE DATABASE flaskAPI;
    ```
    Setup the database url in config
    ```
    mysql+pymysql://root:''@localhost/flaskAPI
    ```

5. Initial, migrate, upgrade db
    ```bash
    flask db init
    ```
    ```bash
    flask db migrate -m "initial migrate"
    ```
    ```bash
    flask db upgrade
    ```

5. Import the POSTMAN Collection to POSTMAN for testing the API.
    ```
    FLASK API.postman_collection.json
    ```    

## API Usage

### User CRUD

- Create User
- Update User
- Get All Users
- Get User by ID
- Delete User

### Movie CRUD

- Create Movie
- Update Movie
- Get All Movies
- Get Movie by ID
- Delete Movie

### Age Ratings CRUD

- Create Age Rating
- Update Age Rating
- Get All Age Ratings
- Get Age Rating by ID
- Delete Age Rating

### Management of User Movies

- User Add Favorite Movie (access Token)

param
```
http://localhost:5030/management/SelectMovie
```
body
```
{
    "user_id" : 7,
    "movie_id": 1,
    "review" : "Soo good!"
}
```
- User View All Favorite Movies (access Token)

param
```
http://localhost:5030/management/GetAllSelectedMovie/7
```
- User Remove Favorite Movie (access Token)

param
```
http://localhost:5030/management/RemoveSelectedMovie/9/1
```
- User Update Movie Review (access Token)

param
```
http://localhost:5030/management/UpdateSelectedMovie/2/1
```
body
```
{
    "review" : "keren bangett"
}
```
- View Movies Added by Users

param
```
http://localhost:5030/management/GetAllMovieUser/1
```
### Authentication

- Register
- Login
- Authentication (Refresh Token)

## Commit Updates

### 22 October 2023

- First Commit

### 23 October 2023

- Add exported POSTMAN JSON for testing
- Fix authentication
- Add authentication in management API
