import requests

from src.abs_classes import JobsParser


class HeadHunterAPI(JobsParser):

    def get_vacancies(self):
        """Осуществляет поиск вакансий по ключевому слову и сохраняет вакансии в список"""
        employers_id = ["15478", "9498120", "80", "4181", "1102601",
                        "3529", "78638", "1740", "3127", "2180"]
        vacancies_list = []

        try:
            for employer in employers_id:
                params = {"employer_id": employer, "only_with_salary": "true", "page": 0, "per_page": 100}
                response = requests.get("https://api.hh.ru/vacancies", params=params)
                data = response.json()["items"]

                for vacancy in data:
                    salary_from = vacancy["salary"]["from"]
                    if not salary_from:
                        salary_from = 0

                    salary_to = vacancy["salary"]["to"]
                    if not salary_to:
                        salary_to = 0

                    vacancy_dict = {"id": vacancy["id"],
                                    "name": vacancy["name"],
                                    "vacancy_url": vacancy["alternate_url"],
                                    "type": vacancy["type"]["name"],
                                    "employer_id": employer,
                                    "employer_name": vacancy["employer"]["name"],
                                    "employer_url": vacancy["employer"]["alternate_url"],
                                    "area": vacancy["area"]["name"],
                                    "salary_from": salary_from,
                                    "salary_to": salary_to,
                                    "schedule": vacancy["schedule"]["name"],
                                    "employment_type": vacancy["employment"]["name"],
                                    "requirements": vacancy["snippet"]["requirement"]}
                    vacancies_list.append(vacancy_dict)
            return vacancies_list

        except (requests.exceptions.HTTPError, ValueError, KeyError) as e:
            raise Exception(e)
