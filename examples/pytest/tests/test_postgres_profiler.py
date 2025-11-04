"""
Simple test for PostgreSQL database profiler
"""
import pytest
import os
from qase.pytest import qase


@qase.id(200)
@qase.title("PostgreSQL Database Profiler Test")
@qase.description("Simple test to verify PostgreSQL database profiler functionality")
@qase.severity("normal")
@qase.priority("high")
def test_postgres_profiler():
    """Test PostgreSQL database operations with profiler."""
    try:
        import psycopg2
    except ImportError:
        pytest.skip("psycopg2 not installed")
    
    # Get connection parameters from environment variables or use defaults
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "testdb")
    db_user = os.getenv("POSTGRES_USER", "testuser")
    db_password = os.getenv("POSTGRES_PASSWORD", "testpass")
    
    conn = None
    cursor = None
    
    try:
        # Connect to PostgreSQL
        with qase.step("Connect to PostgreSQL database"):
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
        
        cursor = conn.cursor()
        
        # Create table
        with qase.step("Create users table"):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Insert data
        with qase.step("Insert test users"):
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                ("John Doe", "john@example.com")
            )
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                ("Jane Smith", "jane@example.com")
            )
        
        # Select data
        with qase.step("Query all users"):
            cursor.execute("SELECT * FROM users ORDER BY id")
            users = cursor.fetchall()
            assert len(users) == 2, f"Expected 2 users, got {len(users)}"
        
        # Update data
        with qase.step("Update user email"):
            cursor.execute(
                "UPDATE users SET email = %s WHERE name = %s",
                ("john.doe@example.com", "John Doe")
            )
            assert cursor.rowcount == 1
        
        # Select specific user
        with qase.step("Query updated user"):
            cursor.execute("SELECT * FROM users WHERE name = %s", ("John Doe",))
            user = cursor.fetchone()
            assert user is not None
            assert user[2] == "john.doe@example.com"
        
        # Delete data
        with qase.step("Delete user"):
            cursor.execute("DELETE FROM users WHERE name = %s", ("Jane Smith",))
            assert cursor.rowcount == 1
        
        # Verify final state
        with qase.step("Verify final user count"):
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            assert count == 1, f"Expected 1 user, got {count}"
        
        # Commit transaction
        conn.commit()
        
    except psycopg2.OperationalError as e:
        pytest.skip(f"PostgreSQL not available: {e}")
    except Exception as e:
        pytest.fail(f"Test failed with error: {e}")
    finally:
        # Clean up: drop table and close connections
        if cursor is not None:
            try:
                # Try to drop table only if connection is still valid
                if conn is not None and not conn.closed:
                    try:
                        cursor.execute("DROP TABLE IF EXISTS users")
                        conn.commit()
                    except Exception:
                        # If drop fails, try to rollback
                        try:
                            conn.rollback()
                        except Exception:
                            pass
            except Exception:
                pass
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass
        if conn is not None:
            try:
                if not conn.closed:
                    conn.close()
            except Exception:
                pass

