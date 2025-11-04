# Database Profiler

## Overview

The Database Profiler automatically tracks and logs all database operations during test execution. It captures database queries, execution times, and connection information, then sends this data as steps to Qase TestOps for detailed analysis and debugging.

## Supported Databases

The profiler supports the following database libraries:

- **SQLite** - Built-in Python module (`sqlite3`)
- **PostgreSQL** - Via `psycopg2` or `psycopg2-binary`
- **MySQL** - Via `pymysql`
- **MongoDB** - Via `pymongo`
- **Redis** - Via `redis` (redis-py)

## Configuration

### Enable Database Profiler

Add `"db"` to the `profilers` array in your `qase.config.json`:

```json
{
  "profilers": ["db"]
}
```

### Multiple Profilers

You can enable multiple profilers simultaneously:

```json
{
  "profilers": ["db", "network", "sleep"]
}
```

## Collected Data

For each database operation, the profiler collects the following information:

### Query Information

- **query** - The actual database query or operation (e.g., SQL statement, Redis command, MongoDB operation)
- **database_type** - Type of database (e.g., "PostgreSQL (psycopg2)", "MongoDB (pymongo)", "Redis")

### Performance Metrics

- **execution_time** - Time taken to execute the query (in seconds, with millisecond precision)
- **rows_affected** - Number of rows affected by the operation (when applicable)

### Connection Information

- **connection_info** - Database connection details (host, port, database name, etc.)

### Error Information

- **error** - Error message if the operation failed (only when `track_on_fail` is enabled)

## Data Format in Qase TestOps

When sent to Qase TestOps, database operations appear as test steps with the following structure:

- **Action**: `[Database Type] query` (e.g., `[PostgreSQL (psycopg2)] SELECT * FROM users`)
- **Input Data**: Connection info, execution time, and rows affected formatted as:

  ```
  Connection: PostgreSQL: localhost | Execution time: 0.123s | Rows affected: 5
  ```

- **Status**: `passed` or `failed` (based on operation success)

## Track on Fail

By default, the profiler tracks database operations even when they fail. You can disable this behavior:

```python
from qase.commons.profilers.db import DatabaseProfilerSingleton
from qase.commons.models.runtime import Runtime

runtime = Runtime()
DatabaseProfilerSingleton.init(runtime=runtime, track_on_fail=False)
```

## Examples

### SQL Query Example

```python
import psycopg2

conn = psycopg2.connect(host="localhost", database="testdb", user="user", password="pass")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = %s", (1,))
users = cursor.fetchall()
```

**Collected Data:**

- Query: `SELECT * FROM users WHERE id = %s`
- Database Type: `PostgreSQL (psycopg2)`
- Execution Time: `0.045s`
- Connection Info: `PostgreSQL: localhost`
- Rows Affected: `1`

### MongoDB Operation Example

```python
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.testdb
collection = db.users
collection.insert_one({"name": "John", "email": "john@example.com"})
```

**Collected Data:**

- Query: `insert_one({'name': 'John', 'email': 'john@example.com'})`
- Database Type: `MongoDB (pymongo)`
- Execution Time: `0.012s`
- Connection Info: `MongoDB: testdb.users`
- Rows Affected: `1`

### Redis Command Example

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('key', 'value')
value = r.get('key')
```

**Collected Data:**

- Query: `SET key value`
- Database Type: `Redis`
- Execution Time: `0.003s`
- Connection Info: `Redis: localhost:6379`

## MongoDB Operations Tracked

For MongoDB, the following operations are automatically tracked:

- `find()` - Find multiple documents
- `find_one()` - Find a single document
- `insert_one()` - Insert a single document
- `update_one()` - Update a single document
- `delete_one()` - Delete a single document

## Redis Operations Tracked

For Redis, all commands executed through `execute_command()` are tracked, including:

- String operations: `SET`, `GET`, `DEL`, etc.
- List operations: `LPUSH`, `RPOP`, `LRANGE`, etc.
- Hash operations: `HSET`, `HGET`, `HGETALL`, etc.
- Set operations: `SADD`, `SMEMBERS`, etc.
- And all other Redis commands

## SQLAlchemy Support

When using SQLAlchemy, all database operations are tracked automatically through SQLAlchemy's event system:

```python
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://user:pass@localhost/db')
with engine.connect() as conn:
    conn.execute(text("SELECT * FROM users"))
```

**Collected Data:**

- Query: `SELECT * FROM users | params: None`
- Database Type: `SQLAlchemy`
- Execution Time: `0.056s`
- Connection Info: `SQLAlchemy Engine: postgresql://user:***@localhost/db`
- Rows Affected: `5`

## Automatic Integration

The database profiler works automatically once enabled in the configuration. No additional code changes are required - it intercepts database operations transparently using monkey patching and proxy classes.

## Notes

- The profiler only tracks operations that occur after it's enabled
- Failed operations are tracked by default (can be disabled with `track_on_fail=False`)
- The profiler handles errors gracefully and won't break your database operations
- All timing measurements have millisecond precision
- Connection information is extracted safely with fallbacks if extraction fails
