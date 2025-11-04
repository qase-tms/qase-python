"""
Simple test for SQLite database profiler
"""
import pytest
import sqlite3
import tempfile
import os
from qase.pytest import qase


@qase.id(201)
@qase.title("SQLite Database Profiler Test")
@qase.description("Simple test to verify SQLite database profiler functionality")
@qase.severity("normal")
@qase.priority("high")
def test_sqlite_profiler():
    """Test SQLite database operations with profiler."""
    # Create a temporary database file
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    conn = None
    cursor = None
    
    try:
        # Connect to SQLite
        with qase.step("Connect to SQLite database"):
            conn = sqlite3.connect(db_path)
        
        cursor = conn.cursor()
        
        # Create table
        with qase.step("Create users table"):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Insert data
        with qase.step("Insert test users"):
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                ("John Doe", "john@example.com")
            )
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
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
                "UPDATE users SET email = ? WHERE name = ?",
                ("john.doe@example.com", "John Doe")
            )
            assert cursor.rowcount == 1
        
        # Select specific user
        with qase.step("Query updated user"):
            cursor.execute("SELECT * FROM users WHERE name = ?", ("John Doe",))
            user = cursor.fetchone()
            assert user is not None
            assert user[2] == "john.doe@example.com"
        
        # Delete data
        with qase.step("Delete user"):
            cursor.execute("DELETE FROM users WHERE name = ?", ("Jane Smith",))
            assert cursor.rowcount == 1
        
        # Verify final state
        with qase.step("Verify final user count"):
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            assert count == 1, f"Expected 1 user, got {count}"
        
        # Commit transaction
        conn.commit()
        
    except Exception as e:
        pytest.fail(f"Test failed with error: {e}")
    finally:
        # Clean up: close connections and remove database file
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
        # Remove temporary database file
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except Exception:
                pass

