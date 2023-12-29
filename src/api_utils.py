import requests

from .abs_classes import JobsParser


class HeadHunterAPI(JobsParser):

    employers_id = ["15478", "9498120", "80", "4181", "1102601",
                    "3529", "78638", "1740", "3127", "2180"]

    def get_employers(self):
        """Осуществляет поиск информации о работодателе"""
        employers_list = []
        try:
            for employer in self.employers_id:
                # response = requests.get(f"https://api.hh.ru/employers/")
                # data = response.json()

                params = {"employer_id": employer, "only_with_salary": "true", "page": 0, "per_page": 1}
                response = requests.get("https://api.hh.ru/vacancies", params=params)
                data = response.json()["items"][0]

                employer_data = {"id": data["employer"]["id"],
                                 "name": data["employer"]["name"],
                                 "url": data["employer"]["alternate_url"]
                                 }
                employers_list.append(employer_data)
            return employers_list

        except (requests.exceptions.HTTPError, ValueError, KeyError) as e:
            raise Exception(e)

    def get_vacancies(self):
        """Осуществляет поиск вакансий по ключевому слову и сохраняет вакансии в список"""
        vacancies_list = []

        try:
            for employer in self.employers_id:
                params = {"employer_id": employer, "only_with_salary": "true", "page": 0, "per_page": 100}
                response = requests.get("https://api.hh.ru/vacancies", params=params)
                data = response.json()["items"]

                for vacancy in data:
                    salary_from = vacancy["salary"]["from"]
                    if not salary_from:
                        salary_from = 0

                    salary_to = vacancy["salary"]["to"]
                    if not salary_to:
                        salary_to = salary_from

                    vacancy_dict = {"id": vacancy["id"],
                                    "name": vacancy["name"],
                                    "vacancy_url": vacancy["alternate_url"],
                                    "type": vacancy["type"]["name"],
                                    "employer_id": employer,
                                    "area": vacancy["area"]["name"],
                                    "salary_from": salary_from,
                                    "salary_to": salary_to,
                                    "salary_currency": vacancy["salary"]["currency"],
                                    "schedule": vacancy["schedule"]["name"],
                                    "employment_type": vacancy["employment"]["name"],
                                    "requirements": vacancy["snippet"]["requirement"]}
                    vacancies_list.append(vacancy_dict)
            return vacancies_list

        except (requests.exceptions.HTTPError, ValueError, KeyError) as e:
            raise Exception(e)
