import sqlite3
import functools

# Global cache dictionary
query_cache = {}

def with_db_connection(func):
    """Decorator to open and close the DB connection, passing it to the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Decorator to cache query results based on the SQL query string argument.
    Caches per-query-string, not per-function-call.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Find the SQL query string for caching
        # It's expected as 'query' in kwargs, or as the second positional argument (after conn)
        query_str = kwargs.get('query')
        if query_str is None and len(args) >= 2:
            query_str = args[1]
        if query_str is None:
            raise ValueError("No SQL query string found for caching.")

        if query_str in query_cache:
            print(f"Using cached result for query: {query_str}")
            return query_cache[query_str]

        print(f"Query not cached, executing: {query_str}")
        result = func(*args, **kwargs)
        query_cache[query_str] = result
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    # First call: should execute and cache
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call result:", users)

    # Second call: should use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call result:", users_again)
