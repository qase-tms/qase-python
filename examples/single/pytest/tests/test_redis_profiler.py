"""
Simple test for Redis database profiler
"""
import pytest
import os
from qase.pytest import qase


@qase.id(204)
@qase.title("Redis Database Profiler Test")
@qase.description("Simple test to verify Redis database profiler functionality")
@qase.severity("normal")
@qase.priority("high")
def test_redis_profiler():
    """Test Redis database operations with profiler."""
    try:
        import redis
    except ImportError:
        pytest.skip("redis not installed")
    
    # Get connection parameters from environment variables or use defaults
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_password = os.getenv("REDIS_PASSWORD", None)
    
    r = None
    
    try:
        # Connect to Redis
        with qase.step("Connect to Redis database"):
            if redis_password:
                r = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    password=redis_password,
                    decode_responses=True
                )
            else:
                r = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    decode_responses=True
                )
            
            # Test connection
            r.ping()
        
        # String operations
        with qase.step("Set key-value pair"):
            r.set("test_key", "test_value")
        
        with qase.step("Get key-value pair"):
            value = r.get("test_key")
            assert value == "test_value", f"Expected 'test_value', got '{value}'"
        
        with qase.step("Update key-value pair"):
            r.set("test_key", "updated_value")
            value = r.get("test_key")
            assert value == "updated_value", f"Expected 'updated_value', got '{value}'"
        
        # List operations
        with qase.step("List push operations"):
            r.lpush("test_list", "item1", "item2", "item3")
        
        with qase.step("List range operation"):
            items = r.lrange("test_list", 0, -1)
            assert len(items) == 3, f"Expected 3 items, got {len(items)}"
        
        with qase.step("List pop operation"):
            item = r.rpop("test_list")
            assert item == "item1", f"Expected 'item1', got '{item}'"
        
        # Hash operations
        with qase.step("Hash set operation"):
            r.hset("test_hash", mapping={"field1": "value1", "field2": "value2"})
        
        with qase.step("Hash get operation"):
            value = r.hget("test_hash", "field1")
            assert value == "value1", f"Expected 'value1', got '{value}'"
        
        with qase.step("Hash get all operation"):
            all_fields = r.hgetall("test_hash")
            assert len(all_fields) == 2, f"Expected 2 fields, got {len(all_fields)}"
        
        # Set operations
        with qase.step("Set add operation"):
            r.sadd("test_set", "member1", "member2", "member3")
        
        with qase.step("Set members operation"):
            members = r.smembers("test_set")
            assert len(members) == 3, f"Expected 3 members, got {len(members)}"
        
        # Delete operations
        with qase.step("Delete key"):
            deleted = r.delete("test_key")
            assert deleted == 1
        
        with qase.step("Verify key is deleted"):
            value = r.get("test_key")
            assert value is None, f"Expected None, got '{value}'"
        
        # Verify final state
        with qase.step("Verify remaining keys"):
            keys = r.keys("test_*")
            assert len(keys) >= 3, f"Expected at least 3 test keys, got {len(keys)}"
        
    except redis.ConnectionError as e:
        pytest.skip(f"Redis not available: {e}")
    except Exception as e:
        pytest.fail(f"Test failed with error: {e}")
    finally:
        # Clean up: delete all test keys
        if r is not None:
            try:
                # Delete all test keys
                test_keys = r.keys("test_*")
                if test_keys:
                    r.delete(*test_keys)
            except Exception:
                pass

