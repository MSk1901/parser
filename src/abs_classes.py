from abc import ABC, abstractmethod


class JobsParser(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass
