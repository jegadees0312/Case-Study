from util.db_conn_util import DBConnUtil
from exceptions.custom_exceptions import EmployeeNotFoundException, PayrollGenerationException, TaxCalculationException, \
    FinancialRecordException, InvalidInputException, DatabaseConnectionException
from entity.employee import Employee
from entity.FinancialRecord import FinancialRecord
from entity.tax import Tax
from entity.payroll import Payroll
from dao.IPayrollService import IPayrollService
from dao.IEmployeeService import IEmployeeService
from dao.IFinancialRecordService import IFinancialRecordService
from dao.ITaxService import ITaxService

class EmployeeService(IEmployeeService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def get_employee_by_id(self, employee_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Employee WHERE EmployeeID = %s", (employee_id,))
            employee_data = cursor.fetchone()
            cursor.close()

            if employee_data:
                return Employee(*employee_data)
            else:
                raise EmployeeNotFoundException("Employee not found with ID: " + str(employee_id))
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving employee from database: " + str(e))

    def get_all_employees(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Employee")
            employees_data = cursor.fetchall()
            cursor.close()


            employees = []
            for employee_data in employees_data:
                employees.append(Employee(*employee_data))

            return employees
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving employees from database: " + str(e))

    def add_employee(self, employee_data):
        try:
            if not employee_data:
                raise InvalidInputException("Employee data is empty")

            cursor = self.connection.cursor()
            insert_query = ("INSERT INTO Employee (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, JoiningDate, TerminationDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(insert_query, (
                employee_data.first_name, employee_data.last_name, employee_data.date_of_birth, employee_data.gender,
                employee_data.email, employee_data.phone_number, employee_data.address, employee_data.position,
                employee_data.joining_date, employee_data.termination_date))
            self.connection.commit()
            cursor.close()
            self.connection.close()

            return "Employee added successfully"
        except Exception as e:
            raise DatabaseConnectionException("Error adding employee to database: " + str(e))

    def update_employee(self, employee_data):
        try:
            if not employee_data:
                raise InvalidInputException("Employee data is empty")

            cursor = self.connection.cursor()
            update_query = "UPDATE Employee SET FirstName=%s, LastName=%s, DateOfBirth=%s, Gender=%s, Email=%s, PhoneNumber=%s, Address=%s, Position=%s, JoiningDate=%s, TerminationDate=%s WHERE EmployeeID=%s"
            cursor.execute(update_query, (
                employee_data.first_name, employee_data.last_name, employee_data.date_of_birth, employee_data.gender,
                employee_data.email, employee_data.phone_number, employee_data.address, employee_data.position,
                employee_data.joining_date, employee_data.termination_date, employee_data.employee_id))
            self.connection.commit()
            cursor.close()
            self.connection.close()

            return "Employee updated successfully"
        except Exception as e:
            raise DatabaseConnectionException("Error updating employee in database: " + str(e))

    def remove_employee(self, employee_id):
        try:
            #connection = get_connection()
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM Employee WHERE EmployeeID = %s"
            cursor.execute(delete_query, (employee_id,))
            self.connection.commit()
            cursor.close()
            self.connection.close()

            return "Employee removed successfully"
        except Exception as e:
            raise DatabaseConnectionException("Error removing employee from database: " + str(e))

class PayrollService(IPayrollService):
    def __init__(self):
        self.connection=DBConnUtil.get_connection()

    def generate_payroll(self, employee_id, start_date, end_date):
        try:
            cursor = self.connection.cursor()
            payroll_data = cursor.execute("SELECT * FROM Payroll WHERE EmployeeID = %s AND PayPeriodStartDate >= %s AND PayPeriodEndDate <= %s", (employee_id, start_date, end_date))
            cursor.close()
            self.connection.close()

            if payroll_data:
                return Payroll(*payroll_data)
            else:
                raise PayrollGenerationException("Payroll data not found for employee ID: " + str(employee_id))
        except Exception as e:
            raise DatabaseConnectionException("Error generating payroll: " + str(e))

    def get_payroll_by_id(self, payroll_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Payroll WHERE PayrollID = %s", (payroll_id,))
            payroll_data = cursor.fetchone()
            cursor.close()
            self.connection.close()

            if payroll_data:
                return Payroll(*payroll_data)
            else:
                raise PayrollGenerationException("Payroll not found with ID: " + str(payroll_id))
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving payroll from database: " + str(e))

    def get_payrolls_for_employee(self, employee_id):
        try:
            #connection = get_connection()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Payroll WHERE EmployeeID = %s", (employee_id,))
            payrolls_data = cursor.fetchall()
            cursor.close()
            self.connection.close()

            payrolls = []
            for payroll_data in payrolls_data:
                payrolls.append(Payroll(*payroll_data))

            return payrolls
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving payrolls from database: " + str(e))

    def get_payrolls_for_period(self, start_date, end_date):
        try:
            #connection = get_connection()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Payroll WHERE PayPeriodStartDate >= %s AND PayPeriodEndDate <= %s", (start_date, end_date))
            payrolls_data = cursor.fetchall()
            cursor.close()
            self.connection.close()

            payrolls = []
            for payroll_data in payrolls_data:
                payrolls.append(Payroll(*payroll_data))

            return payrolls
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving payrolls from database: " + str(e))

class TaxService(ITaxService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def calculate_tax(self, employee_id, tax_year):
        try:
            cursor = self.connection.cursor()
            tax_data = cursor.execute("SELECT * FROM Tax WHERE EmployeeID = %s AND TaxYear = %s", (employee_id, tax_year))
            cursor.close()
            self.connection.close()

            if tax_data:
                return Tax(*tax_data)
            else:
                raise TaxCalculationException("Tax data not found for employee ID: " + str(employee_id) + " and Tax Year: " + str(tax_year))
        except Exception as e:
            raise DatabaseConnectionException("Error calculating tax: " + str(e))

    def get_tax_by_id(self, tax_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Tax WHERE TaxID = %s", (tax_id,))
            tax_data = cursor.fetchone()
            cursor.close()
            self.connection.close()

            if tax_data:
                return Tax(*tax_data)
            else:
                raise TaxCalculationException("Tax not found with ID: " + str(tax_id))
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving tax from database: " + str(e))

    def get_taxes_for_employee(self, employee_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Tax WHERE EmployeeID = %s", (employee_id,))
            taxes_data = cursor.fetchall()
            cursor.close()
            self.connection.close()

            taxes = []
            for tax_data in taxes_data:
                taxes.append(Tax(*tax_data))

            return taxes
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving taxes from database: " + str(e))

    def get_taxes_for_year(self, tax_year):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Tax WHERE TaxYear = %s", (tax_year,))
            taxes_data = cursor.fetchall()
            cursor.close()
            self.connection.close()

            taxes = []
            for tax_data in taxes_data:
                taxes.append(Tax(*tax_data))
                return taxes
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving taxes from database: " + str(e))

class FinancialRecordService(IFinancialRecordService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def add_financial_record(self, employee_id, description, amount, record_type):
        try:
            if not description or not amount or not record_type:
                raise InvalidInputException("Invalid input data for adding financial record")

            cursor = self.connection.cursor()
            insert_query = "INSERT INTO FinancialRecord (EmployeeID, RecordDate, Description, Amount, RecordType) VALUES (%s, NOW(), %s, %s, %s)"
            cursor.execute(insert_query, (employee_id, description, amount, record_type))
            self.connection.commit()
            cursor.close()
            self.connection.close()

            return "Financial record added successfully"
        except Exception as e:
            raise DatabaseConnectionException("Error adding financial record: " + str(e))

    def get_financial_record_by_id(self, record_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM FinancialRecord WHERE RecordID = %s", (record_id,))
            financial_record_data = cursor.fetchone()
            cursor.close()
            self.connection.close()

            if financial_record_data:
                financialrec = FinancialRecord(*financial_record_data)
                return financialrec
            else:
                raise FinancialRecordException("Financial record not found with ID: " + str(record_id))
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving financial record from database: " + str(e))

    def get_financial_records_for_employee(self, employee_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM FinancialRecord WHERE EmployeeID = %s", (employee_id,))
            financial_records_data = cursor.fetchall()
            cursor.close()
            self.connection.close()

            financial_records = []
            for financial_record_data in financial_records_data:
                financial_records.append(FinancialRecord(*financial_record_data))

            return financial_records
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving financial records from database: " + str(e))

    def get_financial_records_for_date(self, record_date):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM FinancialRecord WHERE RecordDate = %s", (record_date,))
            financial_records_data = cursor.fetchall()
            cursor.close()
            self.connection.close()

            financial_records = []
            for financial_record_data in financial_records_data:
                financial_records.append(FinancialRecord(*financial_record_data))

            return financial_records
        except Exception as e:
            raise DatabaseConnectionException("Error retrieving financial records from database: " + str(e))
