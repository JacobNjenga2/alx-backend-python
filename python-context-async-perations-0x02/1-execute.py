import sqlite3

class ExecuteQuery:
    """Context manager to execute a parameterized query and manage connection/cleanup."""
    def __init__(self, query, params=None, db_file='users.db'):
        self.db_file = db_file
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return False  # Don't suppress exceptions

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    with ExecuteQuery(query, param) as results:
        for row in results:
            print(row)

