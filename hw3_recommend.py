import hw3_api as api


API = api.RedisAPI()

API.add_node("Emily", 'Person')
API.add_node("Spencer", 'Person')
API.add_node("Brendan", 'Person')
API.add_node("Trevor", 'Person')
API.add_node("Paxton", 'Person')
API.add_node("Cosmos", 'Book')
API.add_node("Database Design", 'Book')
API.add_node("The Life of Cronkite", 'Book')
API.add_node("DNA and you", 'Book')

API.add_edge("Emily", 'Database Design', "bought")
API.add_edge("Spencer", 'Cosmos', "bought")
API.add_edge("Spencer", 'Database Design', "bought")
API.add_edge("Brendan", 'Database Design', "bought")
API.add_edge("Brendan", 'DNA and you', "bought")
API.add_edge("Trevor", 'Cosmos', "bought")
API.add_edge("Trevor", 'Database Design', "bought")
API.add_edge("Paxton", 'Database Design', "bought")
API.add_edge("Paxton", 'The Life of Cronkite', "bought")
API.add_edge("Emily", 'Spencer', "knows")
API.add_edge("Spencer", 'Emily', "knows")
API.add_edge("Spencer", 'Brendan', "knows")

spencer_recommendations = API.get_recommendations("Spencer")

print(f"Spencer is recommended to buy the book: {spencer_recommendations}")
