# Movie API Documentation

## Getting Started

1. Create a new virtual environment:

    ```bash
    python -m venv env
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Import the POSTMAN Collection "FLASK API.postman_collection.json" to POSTMAN for testing the API.

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
