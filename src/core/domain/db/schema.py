from typing import Protocol, Any, List

class MongoDBRepository(Protocol):
    """
    Protocol defining the contract for a repository that connects to MongoDB.
    This interface specifies the methods that must be implemented by any class
    that wants to serve as a MongoDB repository in the application.
    """

    def connect(self) -> None:
        """
        Establishes a connection to the MongoDB database.
        """
        ...

    def disconnect(self) -> None:
        """
        Closes the connection to the MongoDB database.
        """
        ...

    def insert_one(self, collection: str, document: dict) -> Any:
        """
        Inserts a single document into the specified collection.

        Args:
            collection (str): The name of the collection to insert into.
            document (dict): The document to be inserted.

        Returns:
            Any: The result of the insertion operation.
        """
        ...

    def insert_many(self, collection: str, documents: List[dict]) -> Any:
        """
        Inserts multiple documents into the specified collection.

        Args:
            collection (str): The name of the collection to insert into.
            documents (List[dict]): The list of documents to be inserted.

        Returns:
            Any: The result of the insertion operation.
        """
        ...

    def find_one(self, collection: str, query: dict) -> dict:
        """
        Finds a single document in the specified collection that matches the query.

        Args:
            collection (str): The name of the collection to search in.
            query (dict): The query to filter documents.

        Returns:
            dict: The matching document, or None if no document is found.
        """
        ...

    def find_many(self, collection: str, query: dict) -> List[dict]:
        """
        Finds multiple documents in the specified collection that match the query.

        Args:
            collection (str): The name of the collection to search in.
            query (dict): The query to filter documents.

        Returns:
            List[dict]: A list of matching documents.
        """
        ...

    def update_one(self, collection: str, query: dict, update: dict) -> Any:
        """
        Updates a single document in the specified collection that matches the query.

        Args:
            collection (str): The name of the collection to update.
            query (dict): The query to find the document to update.
            update (dict): The update operations to apply to the document.

        Returns:
            Any: The result of the update operation.
        """
        ...

    def update_many(self, collection: str, query: dict, update: dict) -> Any:
        """
        Updates multiple documents in the specified collection that match the query.

        Args:
            collection (str): The name of the collection to update.
            query (dict): The query to find the documents to update.
            update (dict): The update operations to apply to the documents.

        Returns:
            Any: The result of the update operation.
        """
        ...

    def delete_one(self, collection: str, query: dict) -> Any:
        """
        Deletes a single document from the specified collection that matches the query.

        Args:
            collection (str): The name of the collection to delete from.
            query (dict): The query to find the document to delete.

        Returns:
            Any: The result of the delete operation.
        """
        ...

    def delete_many(self, collection: str, query: dict) -> Any:
        """
        Deletes multiple documents from the specified collection that match the query.

        Args:
            collection (str): The name of the collection to delete from.
            query (dict): The query to find the documents to delete.

        Returns:
            Any: The result of the delete operation.
        """
        ...

