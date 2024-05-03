from dao.impl import EmployeeService, PayrollService, TaxService, FinancialRecordService
from exceptions.custom_exceptions import EmployeeNotFoundException, PayrollGenerationException, TaxCalculationException, \
    FinancialRecordException, InvalidInputException, DatabaseConnectionException
from entity.employee import Employee
from entity.FinancialRecord import FinancialRecord
from entity.tax import Tax
from entity.payroll import Payroll
from datetime import datetime

class MainModule:
    def __init__(self):
        self.employee_service = EmployeeService()
        self.payroll_service = PayrollService()
        self.tax_service = TaxService()
        self.financial_record_service = FinancialRecordService()

    def run(self):
        while True:
            self.main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.employee_management()
            elif choice == '2':
                self.payroll_processing()
            elif choice == '3':
                self.tax_calculation()
            elif choice == '4':
                self.financial_reporting()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def main_menu(self):
        print("\n=== Main Menu ===")
        print("1. Employee Management")
        print("2. Payroll Processing")
        print("3. Tax Calculation")
        print("4. Financial Reporting")
        print("5. Exit")

    def employee_management(self):
        while True:
            self.employee_menu()
            emp_choice = input("Enter your choice: ").strip()

            if emp_choice == '1':
                self.get_employee_by_id()
            elif emp_choice == '2':
                self.get_all_employees()
            elif emp_choice == '3':
                self.add_employee()
            elif emp_choice == '4':
                self.update_employee()
            elif emp_choice == '5':
                self.remove_employee()
            elif emp_choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def employee_menu(self):
        print("\n=== Employee Management Menu ===")
        print("1. Get Employee by ID")
        print("2. Get All Employees")
        print("3. Add Employee")
        print("4. Update Employee")
        print("5. Remove Employee")
        print("6. Back to Main Menu")

    def get_employee_by_id(self):
        emp_id = input("Enter Employee ID: ").strip()
        try:
            employee = self.employee_service.get_employee_by_id(int(emp_id))
            print("Employee:", employee)
        except EmployeeNotFoundException as e:
            print("Error:", e)

    def get_all_employees(self):
        try:
            employees = self.employee_service.get_all_employees()
            print("Employees:", employees)
        except DatabaseConnectionException as e:
            print("Error:", e)

    def add_employee(self):
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        dob_str = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        gender = input("Enter Gender: ").strip()
        email = input("Enter Email: ").strip()
        phone_number = input("Enter Phone Number: ").strip()
        address = input("Enter Address: ").strip()
        position = input("Enter Position: ").strip()
        joining_date_str = input("Enter Joining Date (YYYY-MM-DD): ").strip()
        joining_date = datetime.strptime(joining_date_str, "%Y-%m-%d")
        termination_date_str = input("Enter Termination Date (YYYY-MM-DD, optional): ").strip()
        termination_date = datetime.strptime(termination_date_str, "%Y-%m-%d") if termination_date_str else None

        new_employee = Employee(None, first_name, last_name, dob, gender, email, phone_number,
                                address, position, joining_date, termination_date)

        try:
            self.employee_service.add_employee(new_employee)
            print("Employee added successfully")
        except (InvalidInputException, DatabaseConnectionException) as e:
            print("Error:", e)

    def update_employee(self):
        emp_id = input("Enter Employee ID to update: ").strip()
        try:
            employee = self.employee_service.get_employee_by_id(int(emp_id))
            if employee:
                employee.first_name = input("Enter First Name: ").strip()
                employee.last_name = input("Enter Last Name: ").strip()

                self.employee_service.update_employee(employee)
                print("Employee updated successfully")
            else:
                print("Employee not found with ID:", emp_id)
        except (EmployeeNotFoundException, InvalidInputException, DatabaseConnectionException) as e:
            print("Error:", e)

    def remove_employee(self):
        emp_id = input("Enter Employee ID to remove: ").strip()
        try:
            self.employee_service.remove_employee(int(emp_id))
            print("Employee removed successfully")
        except (EmployeeNotFoundException, DatabaseConnectionException) as e:
            print("Error:", e)

    def payroll_processing(self):
        while True:
            self.payroll_menu()
            payroll_choice = input("Enter your choice: ").strip()

            if payroll_choice == '1':
                self.generate_payroll()
            elif payroll_choice == '2':
                self.get_payroll_by_id()
            elif payroll_choice == '3':
                self.get_payrolls_for_employee()
            elif payroll_choice == '4':
                self.get_payrolls_for_period()
            elif payroll_choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def payroll_menu(self):
        print("\n=== Payroll Processing Menu ===")
        print("1. Generate Payroll")
        print("2. Get Payroll by ID")
        print("3. Get Payrolls for Employee")
        print("4. Get Payrolls for Period")
        print("5. Back to Main Menu")

    def generate_payroll(self):
        emp_id = input("Enter Employee ID: ").strip()
        start_date_str = input("Enter Pay Period Start Date (YYYY-MM-DD): ").strip()
        end_date_str = input("Enter Pay Period End Date (YYYY-MM-DD): ").strip()

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            payroll = self.payroll_service.generate_payroll(int(emp_id), start_date, end_date)
            print("Payroll generated successfully:", payroll)
        except (EmployeeNotFoundException, PayrollGenerationException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_payroll_by_id(self):
        payroll_id = input("Enter Payroll ID: ").strip()
        try:
            payroll = self.payroll_service.get_payroll_by_id(int(payroll_id))
            print("Payroll:", payroll)
        except (EmployeeNotFoundException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_payrolls_for_employee(self):
        emp_id = input("Enter Employee ID: ").strip()
        try:
            payrolls = self.payroll_service.get_payrolls_for_employee(int(emp_id))
            print("Payrolls for Employee:", payrolls)
        except (EmployeeNotFoundException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_payrolls_for_period(self):
        start_date_str = input("Enter Pay Period Start Date (YYYY-MM-DD): ").strip()
        end_date_str = input("Enter Pay Period End Date (YYYY-MM-DD): ").strip()

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            payrolls = self.payroll_service.get_payrolls_for_period(start_date, end_date)
            print("Payrolls for Period:", payrolls)
        except DatabaseConnectionException as e:
            print("Error:", e)

    def tax_calculation(self):
        while True:
            self.tax_menu()
            tax_choice = input("Enter your choice: ").strip()

            if tax_choice == '1':
                self.calculate_tax()
            elif tax_choice == '2':
                self.get_tax_by_id()
            elif tax_choice == '3':
                self.get_taxes_for_employee()
            elif tax_choice == '4':
                self.get_taxes_for_year()
            elif tax_choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def tax_menu(self):
        print("\n=== Tax Calculation Menu ===")
        print("1. Calculate Tax")
        print("2. Get Tax by ID")
        print("3. Get Taxes for Employee")
        print("4. Get Taxes for Year")
        print("5. Back to Main Menu")

    def calculate_tax(self):
        emp_id = input("Enter Employee ID: ").strip()
        tax_year = input("Enter Tax Year: ").strip()

        try:
            tax_amount = self.tax_service.calculate_tax(int(emp_id), int(tax_year))
            print("Tax calculated successfully:", tax_amount)
        except (EmployeeNotFoundException, TaxCalculationException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_tax_by_id(self):
        tax_id = input("Enter Tax ID: ").strip()
        try:
            tax = self.tax_service.get_tax_by_id(int(tax_id))
            print("Tax:", tax)
        except (EmployeeNotFoundException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_taxes_for_employee(self):
        emp_id = input("Enter Employee ID: ").strip()
        try:
            taxes = self.tax_service.get_taxes_for_employee(int(emp_id))
            print("Taxes for Employee:", taxes)
        except (EmployeeNotFoundException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_taxes_for_year(self):
        tax_year = input("Enter Tax Year: ").strip()
        try:
            taxes = self.tax_service.get_taxes_for_year(int(tax_year))
            print("Taxes for Year:", taxes)
        except DatabaseConnectionException as e:
            print("Error:", e)

    def financial_reporting(self):
        while True:
            self.financial_menu()
            financial_choice = input("Enter your choice: ").strip()

            if financial_choice == '1':
                self.add_financial_record()
            elif financial_choice == '2':
                self.get_financial_record_by_id()
            elif financial_choice == '3':
                self.get_financial_records_for_employee()
            elif financial_choice == '4':
                self.get_financial_records_for_date()
            elif financial_choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def financial_menu(self):
        print("\n=== Financial Reporting Menu ===")
        print("1. Add Financial Record")
        print("2. Get Financial Record by ID")
        print("3. Get Financial Records for Employee")
        print("4. Get Financial Records for Date")
        print("5. Back to Main Menu")

    def add_financial_record(self):
        emp_id = input("Enter Employee ID: ").strip()
        description = input("Enter Description: ").strip()
        amount = input("Enter Amount: ").strip()
        record_type = input("Enter Record Type: ").strip()

        try:
            financial_record = self.financial_record_service.add_financial_record(int(emp_id), description,
                                                                                  float(amount), record_type)
            print("Financial Record added successfully:", financial_record)
        except (EmployeeNotFoundException, InvalidInputException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_financial_record_by_id(self):
        record_id = input("Enter Record ID: ").strip()
        try:
            financial_record = self.financial_record_service.get_financial_record_by_id(int(record_id))
            print("Financial Record:", financial_record)
        except (FinancialRecordException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_financial_records_for_employee(self):
        emp_id = input("Enter Employee ID: ").strip()
        try:
            financial_records = self.financial_record_service.get_financial_records_for_employee(int(emp_id))
            print("Financial Records for Employee:", financial_records)
        except (EmployeeNotFoundException, DatabaseConnectionException) as e:
            print("Error:", e)

    def get_financial_records_for_date(self):
        record_date_str = input("Enter Record Date (YYYY-MM-DD): ").strip()
        try:
            record_date = datetime.strptime(record_date_str, "%Y-%m-%d")
            financial_records = self.financial_record_service.get_financial_records_for_date(record_date)
            print("Financial Records for Date:", financial_records)
        except (ValueError, DatabaseConnectionException) as e:
            print("Error:", e)

