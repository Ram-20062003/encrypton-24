# Hack-Backend

Fast Api Application

# References

- [FOR CRUD Operations](https://github.com/vnurhaqiqi/fastapi-sqlmodel-postgresql/blob/master/app/main.py#L70)

# Setup

- copy content of .env.example to .env
  ```sh
   cp .env.example .env
  ```  
- Setup the virtualenv
  - Create a virtualenv for this project.
    ```sh
     pipenv install
    ```
  - Activate virtualenv for this project.
    ```sh
     pipenv shell
    ```
  - Install dev dependencies
    ```sh
     pipenv install --dev
    ```
- Docker
  - Build and Up the Docker Container.
    ```sh
    docker-compose up --build
    ```
- To Run Migrations
  - To make Migrations
    ```sh
    docker exec backend_server alembic revision --autogenerate -m <COMMIT_MESSAGE>
    ```
  - To run Migrations
    ```sh
    docker exec backend_server alembic upgrade head
    ```