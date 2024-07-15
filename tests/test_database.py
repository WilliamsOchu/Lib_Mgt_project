import unittest
from app import app, mysql

class TestDatabaseConnection(unittest.TestCase):

## Test to initiate database
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['MYSQL_DB'] = 'test_library_db'
        
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # Set up the test database
        with mysql.connection.cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS test_library_db')
            cursor.execute('USE test_library_db')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL
                )
            ''')
            mysql.connection.commit()
            
            
## Test to destroy database
    def tearDown(self):
        # Clean up the test database
        with mysql.connection.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS test_library_db')
        self.app_context.pop()

## Test to validate database connection
    def test_database_connection(self):
        # Test inserting data
        with mysql.connection.cursor() as cursor:
            cursor.execute('USE test_library_db')
            cursor.execute('INSERT INTO test_table (name) VALUES (%s)', ('Test Name',))
            mysql.connection.commit()

## Test to Query Database Data        
        # Test querying data
        with mysql.connection.cursor() as cursor:
            cursor.execute('USE test_library_db')
            cursor.execute('SELECT name FROM test_table WHERE name = %s', ('Test Name',))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 'Test Name')

if __name__ == '__main__':
    unittest.main()
