import psycopg2

from src.abs_classes import DataHandler, DBExecutor


class PostgresExecutor(DBExecutor):

    def __init__(self, password):
        self.__password = password

    @property
    def password(self):
        return self.__password

    def create_database(self, db_name: str):
        """Creates a database"""
        try:
            conn = psycopg2.connect(
                database="postgres",
                user="postgres",
                password=self.password,
                host="localhost",
                port="5432"
            )

            conn.autocommit = True
            cursor = conn.cursor()

            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {db_name}")

            conn.close()
        except psycopg2.OperationalError as e:
            raise Exception(e)

    def create_table(self, table_name: str):
        """Creates table employers or vacancies"""
        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:

                    if table_name == "employers":
                        cursor.execute("""
                                CREATE TABLE IF NOT EXISTS employers
                                (
                                    employer_id int PRIMARY KEY,
                                    name varchar(100) NOT NULL,
                                    url varchar(255) NOT NULL
                                );
                                """)

                    elif table_name == "vacancies":
                        cursor.execute("""
                                CREATE TABLE IF NOT EXISTS vacancies
                                (
                                    vacancy_id int PRIMARY KEY,
                                    name varchar(100) NOT NULL,
                                    type varchar(20) NOT NULL,
                                    url varchar(255) NOT NULL,
                                    employer_id int REFERENCES employers (employer_id),
                                    area varchar(100) NOT NULL,
                                    salary_from int NOT NULL,
                                    salary_to int NOT NULL,
                                    salary_currency varchar(5) NOT NULL,
                                    schedule varchar(50) NOT NULL,
                                    employment_type varchar(50) NOT NULL,
                                    requirements text
                                );
                                """)
                    else:
                        raise ValueError("Invalid table name")

        except (psycopg2.OperationalError, psycopg2.DatabaseError, psycopg2.InternalError) as e:
            raise Exception(e)

    def insert_values(self, values, table_name: str):
        """Inserts values to employers/vacancies tables"""
        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:
                    if table_name == "employers":
                        for value in values:
                            cursor.execute(f"""
                            INSERT INTO employers VALUES 
                            ({value["id"]}, '{value["name"]}', '{value["url"]}');
                            """)
                    elif table_name == "vacancies":
                        for value in values:
                            cursor.execute(f"""
                            INSERT INTO vacancies VALUES
                            ({value["id"]},
                            '{value["name"]}',
                            '{value["type"]}',
                            '{value["vacancy_url"]}',
                            {value["employer_id"]},
                            '{value["area"]}',
                            {value["salary_from"]},
                            {value["salary_to"]},
                            '{value["salary_currency"]}',
                            '{value["schedule"]}',
                            '{value["employment_type"]}',
                            '{value["requirements"]}'
                            );
                            """)
                    else:
                        raise ValueError("Invalid table name")

        except (psycopg2.OperationalError, psycopg2.DatabaseError,
                psycopg2.InternalError, psycopg2.DataError) as e:
            raise Exception(e)


class DBManager(DataHandler):

    def __init__(self, password):
        self.__password = password

    @property
    def password(self):
        return self.__password

    def get_companies_and_vacancies_count(self):
        """Returns amount of unique companies and vacancies"""
        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM employers")
                    companies_count = cursor.fetchone()[0]

                    cursor.execute("SELECT COUNT(*) FROM vacancies")
                    vacancies_count = cursor.fetchone()[0]

                    data = {"companies_count": companies_count,
                            "vacancies_count": vacancies_count}
                    return data

        except (psycopg2.OperationalError, psycopg2.DatabaseError,
                psycopg2.InternalError, psycopg2.DataError) as e:
            raise Exception(e)

    def get_all_vacancies(self):
        """Returns list of all vacancies"""
        vacancies_parsed = []

        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:
                    cursor.execute("SELECT * FROM vacancies")
                    vacancies = cursor.fetchall()

                    for vacancy in vacancies:
                        vacancy_dict = {"id": vacancy[0],
                                        "name": vacancy[1],
                                        "type": vacancy[2],
                                        "vacancy_url": vacancy[3],
                                        "employer_id": vacancy[4],
                                        "area": vacancy[5],
                                        "salary_from": vacancy[6],
                                        "salary_to": vacancy[7],
                                        "salary_currency": vacancy[8],
                                        "schedule": vacancy[9],
                                        "employment_type": vacancy[10],
                                        "requirements": vacancy[11]}
                        vacancies_parsed.append(vacancy_dict)

            return vacancies_parsed

        except (psycopg2.OperationalError, psycopg2.DatabaseError,
                psycopg2.InternalError, psycopg2.DataError) as e:
            raise Exception(e)

    def get_avg_salary(self):
        """Returns average salary for vacancies in database by currency"""
        average_salaries = []

        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:
                    cursor.execute("""
                    SELECT AVG((salary_from + salary_to) / 2), salary_currency 
                    FROM vacancies
                    GROUP BY salary_currency
                    """)
                    result = cursor.fetchall()

                    for value in result:
                        avg = {"currency": value[1],
                               "average_salary": round(float(value[0]), 2)}

                        average_salaries.append(avg)

            return average_salaries

        except (psycopg2.OperationalError, psycopg2.DatabaseError,
                psycopg2.InternalError, psycopg2.DataError) as e:
            raise Exception(e)

    def get_vacancies_with_higher_salary(self):
        """Returns list of vacancies with the highest salary by currency"""
        vacancies_list = []

        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:
                    cursor.execute("""
                    SELECT DISTINCT ON (salary_currency) 
                    vacancy_id, 
                    name, 
                    url, 
                    salary_from,
                    salary_to,
                    salary_currency
                    FROM vacancies
                    ORDER BY salary_currency, 
                    (salary_to + salary_from) / 2 DESC;
                    """)
                    result = cursor.fetchall()

                    for value in result:
                        avg = {"vacancy_id": value[0],
                               "name": value[1],
                               "url": value[2],
                               "salary_from": value[3],
                               "salary_to": value[4],
                               "salary_currency": value[5]
                               }

                        vacancies_list.append(avg)

            return vacancies_list

        except (psycopg2.OperationalError, psycopg2.DatabaseError,
                psycopg2.InternalError, psycopg2.DataError) as e:
            raise Exception(e)

    def get_vacancies_with_keyword(self, keyword: str):
        """Returns vacancies with a keyword in name or requirements"""
        vacancies_list = []

        try:
            with psycopg2.connect(
                    host="localhost",
                    database="course",
                    user="postgres",
                    password=self.password) as connector:
                with connector.cursor() as cursor:
                    cursor.execute(f"""
                            SELECT * FROM vacancies
                            WHERE name ILIKE '%{keyword}%' 
                            OR requirements ILIKE '%{keyword}%';
                            """)
                    result = cursor.fetchall()

                    for value in result:
                        vacancy = {"vacancy_id": value[0],
                                   "name": value[1],
                                   "type": value[2],
                                   "url": value[3],
                                   "employer_id": value[4],
                                   "area": value[5],
                                   "salary_from": value[6],
                                   "salary_to": value[7],
                                   "salary_currency": value[8],
                                   "schedule": value[9],
                                   "employment_type": value[10],
                                   "requirements": value[11]
                                   }

                        vacancies_list.append(vacancy)

            return vacancies_list

        except (psycopg2.OperationalError, psycopg2.DatabaseError,
                psycopg2.InternalError, psycopg2.DataError) as e:
            raise Exception(e)
