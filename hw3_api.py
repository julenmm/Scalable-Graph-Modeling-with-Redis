import redis


class RedisAPI:
    """
    A class for interacting with a Redis database to manage a graph of nodes and edges.

    Attributes:
        redis_client (redis.StrictRedis): The Redis client for database operations.
    """

    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initializes the RedisAPI instance with a connection to the Redis database.

        Args:
            host (str): The hostname of the Redis server. Defaults to 'localhost'.
            port (int): The port number of the Redis server. Defaults to 6379.
            db (int): The database number to use. Defaults to 0.
        """
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def add_node(self, name, type_):
        """
        Adds a node to the graph with the given name and type.

        Args:
            name (str): The name of the node.
            type_ (str): The type of the node.

        Returns:
            int: The number of fields that were added to the hash.
        """
        key = "node:"
        id_ = self.redis_client.incr(f"id_counter-{key}")
        key = key + str(id_)
        return self.redis_client.hset(key, mapping={"name": name, "type": type_})

    def add_edge(self, name1, name2, type_):
        """
        Adds an edge to the graph connecting two nodes with the given names and type.

        Args:
            name1 (str): The name of the first node.
            name2 (str): The name of the second node.
            type_ (str): The type of the edge.

        Returns:
            int: The number of fields that were added to the hash.
        """
        key = "edge:"
        id_ = self.redis_client.incr(f"id_counter-{key}")
        key = key + str(id_)
        return self.redis_client.hset(key, mapping={"name1": name1, "name2": name2, "type": type_})

    def get_adjacent(self, name, node_type=None, edge_type=None) -> list[dict[str, str]]:
        """
        Retrieves a list of adjacent nodes to the given node, optionally filtered by node and edge types.

        Args:
            name (str): The name of the node to find adjacent nodes for.
            node_type (str, optional): The type of the adjacent nodes to filter by. Defaults to None.
            edge_type (str, optional): The type of the edges to filter by. Defaults to None.

        Returns:
            list[dict[str, str]]: A list of dictionaries representing the adjacent nodes.
        """
        edge_keys = self.redis_client.keys("edge:*")
        adjacent_nodes = []
        for ek in edge_keys:
            current_edge = self.redis_client.hgetall(ek)
            current_edge_type = current_edge["type"]
            node1_name = current_edge["name1"]
            node2_name = current_edge["name2"]

            current_node1_type = self.get_node_type(node1_name)
            current_node2_type = self.get_node_type(node2_name)

            if node1_name == name:
                if (node_type is None or node_type == current_node2_type) and (edge_type is None or edge_type == current_edge_type):
                    adjacent_nodes.append(self.get_node(node2_name))
            elif node2_name == name:
                if (node_type is None or node_type == current_node1_type) and (edge_type is None or edge_type == current_edge_type):
                    adjacent_nodes.append(self.get_node(node1_name))

        return adjacent_nodes

    def get_recommendations(self, name):
        """
        Retrieves book recommendations for a given person based on what their friends have bought.

        Args:
            name (str): The name of the person to get recommendations for.

        Returns:
            list[str]: A list of book names that are recommended.
        """
        friends = self.get_adjacent(name, "Person", "knows")
        print(friends)
        recommendations = []
        already_bought = [book["name"] for book in self.get_adjacent(name, "Book", "bought")]
        for friend in friends:
            friend_books = self.get_adjacent(friend["name"], "Book", "bought")
            for book in friend_books:
                if book["name"] not in already_bought:
                    print("book name", book["name"])
                    recommendations.append(book["name"])
        return recommendations

    # Helper functions bellow

    def get_node(self, name):
        """
        Retrieves the details of a node with the given name.

        Args:
            name (str): The name of the node to retrieve.

        Returns:
            dict[str, str]: A dictionary representing the node.

        Raises:
            Exception: If the node with the given name is not found.
        """
        keys = self.redis_client.keys("node:*")
        for key in keys:
            current_node_name = self.redis_client.hget(key, "name")
            if current_node_name == name:
                return self.redis_client.hgetall(key)

        raise Exception(f"Node with key {name} not found")

    def get_node_type(self, name) -> str:
        """
        Retrieves the type of node with the given name.

        Args:
            name (str): The name of the node to retrieve the type for.

        Returns:
            str: The type of the node.

        Raises:
            Exception: If the node with the given name is not found.
        """
        key = self.get_node_key(name)
        node_type_ = self.redis_client.hget(key, "type")
        return node_type_

    def get_node_key(self, name):
        """
        Retrieves the Redis key for a node with the given name.

        Args:
            name (str): The name of the node to retrieve the key for.

        Returns:
            str: The Redis key for the node.

        Raises:
            Exception: If the node with the given name is not found.
        """
        keys = self.redis_client.keys("node:*")
        for key in keys:
            current_node_name = self.redis_client.hget(key, "name")
            if current_node_name == name:
                return key

        raise Exception(f"Node with key {name} not found")



