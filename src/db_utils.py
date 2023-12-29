import psycopg2

from .abs_classes import DataHandler, DBExecutor


class PostgresExecutor(DBExecutor):

    def __init__(self, password):
        self.__password = password

    @property
    def password(self):
        return self.__password

    def create_database(self, db_name: str):
        pass

    def create_table(self, table_name: str):
        pass

    def insert_values(self, values, table_name: str):
        pass


class DBManager(DataHandler):

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self, keyword: str):
        pass
