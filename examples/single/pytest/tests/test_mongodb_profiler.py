"""
Simple test for MongoDB database profiler
"""
import pytest
import os
from qase.pytest import qase


@qase.id(203)
@qase.title("MongoDB Database Profiler Test")
@qase.description("Simple test to verify MongoDB database profiler functionality")
@qase.severity("normal")
@qase.priority("high")
def test_mongodb_profiler():
    """Test MongoDB database operations with profiler."""
    try:
        from pymongo import MongoClient
    except ImportError:
        pytest.skip("pymongo not installed")
    
    # Get connection parameters from environment variables or use defaults
    db_host = os.getenv("MONGODB_HOST", "localhost")
    db_port = int(os.getenv("MONGODB_PORT", "27017"))
    db_name = os.getenv("MONGODB_DB", "testdb")
    db_user = os.getenv("MONGODB_USER", None)
    db_password = os.getenv("MONGODB_PASSWORD", None)
    
    client = None
    
    try:
        # Connect to MongoDB
        with qase.step("Connect to MongoDB database"):
            if db_user and db_password:
                client = MongoClient(
                    host=db_host,
                    port=db_port,
                    username=db_user,
                    password=db_password,
                    authSource="admin"
                )
            else:
                client = MongoClient(
                    host=db_host,
                    port=db_port
                )
        
        db = client[db_name]
        collection = db.users
        
        # Insert data
        with qase.step("Insert test users"):
            result1 = collection.insert_one({
                "name": "John Doe",
                "email": "john@example.com"
            })
            result2 = collection.insert_one({
                "name": "Jane Smith",
                "email": "jane@example.com"
            })
            assert result1.inserted_id is not None
            assert result2.inserted_id is not None
        
        # Find all documents
        with qase.step("Query all users"):
            users = list(collection.find())
            assert len(users) == 2, f"Expected 2 users, got {len(users)}"
        
        # Find specific document
        with qase.step("Query user by name"):
            user = collection.find_one({"name": "John Doe"})
            assert user is not None
            assert user["email"] == "john@example.com"
        
        # Update document
        with qase.step("Update user email"):
            result = collection.update_one(
                {"name": "John Doe"},
                {"$set": {"email": "john.doe@example.com"}}
            )
            assert result.modified_count == 1
        
        # Verify update
        with qase.step("Query updated user"):
            user = collection.find_one({"name": "John Doe"})
            assert user is not None
            assert user["email"] == "john.doe@example.com"
        
        # Delete document
        with qase.step("Delete user"):
            result = collection.delete_one({"name": "Jane Smith"})
            assert result.deleted_count == 1
        
        # Verify final state
        with qase.step("Verify final user count"):
            count = collection.count_documents({})
            assert count == 1, f"Expected 1 user, got {count}"
        
    except Exception as e:
        # Check if it's a connection error
        error_msg = str(e).lower()
        if "connection" in error_msg or "timeout" in error_msg or "network" in error_msg:
            pytest.skip(f"MongoDB not available: {e}")
        else:
            pytest.fail(f"Test failed with error: {e}")
    finally:
        # Clean up: drop collection and close connection
        if client is not None:
            try:
                db = client[db_name]
                collection = db.users
                collection.drop()
            except Exception:
                pass
            finally:
                try:
                    client.close()
                except Exception:
                    pass

