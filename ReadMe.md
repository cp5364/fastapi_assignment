- First create a virtual environment of you choosing

After that a few more changes are required for the database details:
    1/ Please fill out details of the required DB in the .env file like: 
        POSTGRES_USER
        POSTGRES_PASSWORD
        POSTGRES_SERVER
        POSTGRES_PORT

    2/ Navihgate into "src/utils/config.py" and make the following changes:
        change the POSTGRES_DB default value to the name of your db ( For Postgres)
    


- Then run the following command to install all the required packages in the virtual environment.
:NOTE it has to be done in the project folder not in the src folder
# pip install -r requirements.txt

- Here for migration script management a library called alembic is used.
So, in order to create tables in your local DB following commands need to be fired.

# alembic stamp head
# alembic revision --autogenerate
# alembic upgrade head

- Then to start the backend server, the following command needs to run using uvicorn, and it would start on your local server

# uvicorn src.main:app -- reload

- A few notes on the on the API front:
    1/ As of now you have to manually insert users as JWT tokens are not integrated.

    2/ One user can have only 1 address as the code. 

    3/ The co-ordinated should be passed as a tuple with 2 elemets e.g(-67.369423649,165.3897482734), the first element should be lattitude and the second element should be the longitude of the given address.

    4/The address should be filled out with comma separated strings.

    5/ The distance has to be given in kilometers for the get api where we need to get the address in a     radius.
    
    6/ Docker file and entry point files are also included. Feel free to change and use as per your requirement.
