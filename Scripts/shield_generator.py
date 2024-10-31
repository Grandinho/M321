from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError
from bson import ObjectId

class ShieldGeneratorDB:
    """
    Class to handle MongoDB connection and data retrieval for the shield generator.
    """
    def __init__(self):
        self.connection_string = "mongodb://theship:theship1234@192.168.100.15:2021/theshipdb"
        self.database_name = "theshipdb"
        self.collection_name = "vacuum-energy"
        self.client = None
        self.db = None
        self.collection = None
        # Predefined ObjectId for the vacuum energy document
        self.vacuum_energy_id = ObjectId('6704734d0d529bbe3471b5fe')

    def connect(self):
        """
        Establishes connection to MongoDB.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False
        except OperationFailure as e:
            print(f"Authentication failed: {e}")
            return False

    def get_vacuum_energy_data(self):
        """
        Retrieves vacuum energy sensor data from MongoDB.
        
        Returns:
            str: Hex string of vacuum energy data if successful
            None: If no data found or error occurs
        """
        try:
            if not self.client:
                if not self.connect():
                    return None

            document = self.collection.find_one({})
            if document and "data" in document:
                return document["data"]
            else:
                print("No vacuum energy data found in database")
                return None

        except Exception as e:
            print(f"Error retrieving vacuum energy data: {e}")
            return None

    def update_vacuum_energy_data(self, data):
        """
        Updates or creates the vacuum energy data document.
        Ensures only one document exists in the collection.
        
        Args:
            data (str): Hex string of vacuum energy data
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            if not self.client:
                if not self.connect():
                    return False

            # Validate data format (simple hex string check)
            if not all(c in '0123456789abcdefABCDEF' for c in data):
                print("Invalid data format. Must be a hex string.")
                return False

            # Use upsert to either update existing document or create new one
            result = self.collection.update_one(
                {"_id": self.vacuum_energy_id},
                {"$set": {"data": data}},
                upsert=True
            )

            # If there are other documents in the collection, remove them
            self.collection.delete_many({
                "_id": {"$ne": self.vacuum_energy_id}
            })

            return True

        except Exception as e:
            print(f"Error updating vacuum energy data: {e}")
            return False

    def close(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        """
        Enables use of 'with' statement.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures connection is closed when using 'with' statement.
        """
        self.close()