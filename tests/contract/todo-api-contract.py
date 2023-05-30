import unittest
from pact import Consumer, Provider
from urllib.parse import quote

# Define the consumer and provider names
consumer = Consumer('TodoAppConsumer')
provider = Provider('TodoAppProvider')

# Create a pact between the consumer and provider
pact = consumer.has_pact_with(provider)

# Define the expected request and response for creating a todo
create_todo_request = {
    'method': 'POST',
    'path': '/todos',
    'headers': {'Content-Type': 'application/json'},
    'body': {
        "task": "Wash car",
        "description": "Go to car wash and wash the car",
    }
}

create_todo_response = {
    'status': 201,
    'headers': {'Content-Type': 'application/json'},
    'body': {
        "id": 1,
        "task": "Wash car",
        "description": "Go to car wash and wash the car",
        "completed": False,
    }
}

# Define the expected request and response for getting a todo
get_todo_request = {
    'method': 'GET',
    'path': '/todos/1'
}

get_todo_response = {
    'status': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': {
        "id": 1,
        "task": "Wash car",
        "description": "Go to car wash and wash the car",
        "completed": False,
    }
}

class TodoAppContractTest(unittest.TestCase):

    def test_create_todo_contract(self):
        (pact
         .given('A new todo is created')
         .upon_receiving('a request to create a todo')
         .with_request(**create_todo_request)
         .will_respond_with(**create_todo_response))

    def test_get_todo_contract(self):
        (pact
         .given('A todo exists with ID 1')
         .upon_receiving('a request to get a todo')
         .with_request(**get_todo_request)
         .will_respond_with(**get_todo_response))

    # Run the contract tests
    def test_contract(self):
        self.test_create_todo_contract()
        self.test_get_todo_contract()
        pact.verify()

if __name__ == '__main__':
    unittest.main()
