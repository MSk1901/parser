import os

from src.api_utils import HeadHunterAPI
from src.db_utils import DBManager, PostgresExecutor


def main():
    hh_api = HeadHunterAPI()
    employers_list = hh_api.get_employers()
    vacancies_list = hh_api.get_vacancies()

    password = os.getenv("DB_POSTGRES_PASSWORD")
    psql = PostgresExecutor(password)
    db = DBManager(password)

    psql.create_database("course")
    psql.create_table("employers")
    psql.create_table("vacancies")
    psql.insert_values(employers_list, "employers")
    psql.insert_values(vacancies_list, "vacancies")

    print(db.get_companies_and_vacancies_count())
    print(db.get_all_vacancies())
    print(db.get_avg_salary())
    print(db.get_vacancies_with_higher_salary())

    keyword = input("Enter a keyword to search vacancies: ").strip()
    print(db.get_vacancies_with_keyword(keyword))


if __name__ == '__main__':
    main()
