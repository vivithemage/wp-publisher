import pymysql.cursors

class Database:
    def __init__(self, variables):
        self.variables = variables

    def generate_database_name(self):
        site_url = self.variables['site_url']
        site_url_split = site_url.split('.')
        database_name = site_url_split[0]
        return database_name

    def create_database(self):
        # Connect to the database
        print(self.variables)
        connection = pymysql.connect(host=self.variables['database']['hostname'],
                                     user=self.variables['database']['username'],
                                     password=self.variables['database']['password'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "create database " + self.generate_database_name()
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

