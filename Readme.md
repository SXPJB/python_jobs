# Python Thread

## Pre-requisite
- Python 3.7 or above
- PyCharm or any other IDE
- Basic understanding of Python
- Basic understanding of Threading

## How to run
- Clone the repository
- Open the project in PyCharm
- Create a new Python virtual environment
- Install the requirements using `pip install -r requirements.txt`
- Run the `main.py` file

## How to test
- In postman, make a POST request to `http://localhost:8080/execute` with the following JSON body:
```json
{
    "items": <number of items>
}
```
- To see the all the threads in action, make a GET request to `http://localhost:8080/job`
- To see the status of a particular job, make a GET request to `http://localhost:8080/job/<job_id>`