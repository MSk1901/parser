from abc import ABC, abstractmethod


class JobsParser(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class DataHandler(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str):
        pass


class DBExecutor(ABC):

    @abstractmethod
    def create_database(self, db_name: str):
        pass

    @abstractmethod
    def create_table(self, table_name: str):
        pass

    def insert_values(self, values, table_name: str):
        pass
