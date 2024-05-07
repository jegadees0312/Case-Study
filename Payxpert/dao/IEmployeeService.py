
from abc import ABC, abstractmethod
from entity.employee import Employee
class IEmployeeService(ABC):
    @abstractmethod
    def get_employee_by_id(self, employee_id: int) -> Employee:
        pass

    @abstractmethod
    def get_all_employees(self) -> list[Employee]:
        pass

    @abstractmethod
    def add_employee(self, employee_data: dict) -> bool:
        pass

    @abstractmethod
    def update_employee(self, employee_data: dict) -> bool:
        pass

    @abstractmethod
    def remove_employee(self, employee_id: int) -> bool:
        pass
