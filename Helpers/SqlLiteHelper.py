import sqlite3
from sqlite3 import Error


class SQLiteHelper:
    def __init__(self, db_file):
        """ Initialize the connection to the SQLite database. """
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(f"Error connecting to database: {e}")

    def yield_fetch_all_records(self):
        """ Fetch each record one by one from the section_diagrams table. """
        self.create_connection()
        fetch_sql = "SELECT section_diagram, section_diagram_url FROM section_diagrams;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(fetch_sql)
            for row in cursor:
                yield row
        except Error as e:
            print(f"Error fetching record: {e}")
        finally:
            self.close_connection()

    def fetch_records_by_page(self, page_size: int, offset: int):
        """ Fetch a page of records starting from the specified offset. """
        self.create_connection()
        fetch_sql = "SELECT section_diagram, section_diagram_url FROM section_diagrams LIMIT ? OFFSET ?;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(fetch_sql, (page_size, offset))
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching page: {e}")
            return []
        finally:
            self.close_connection()

    def fetch_total_records(self):
        """ Fetch total record count in section_diagrams table. """
        self.create_connection()
        fetch_sql = "SELECT COUNT(*) FROM section_diagrams;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(fetch_sql)
            count = cursor.fetchone()[0]  # Extract the count from the result
            return count
        except Error as e:
            return 0
        finally:
            self.close_connection()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
