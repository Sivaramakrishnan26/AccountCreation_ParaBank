from pages.register_page import RegisterPage
from selenium.webdriver.common.by import By
from datetime import datetime
from conftest import setup
import pandas as pd
import pytest
import os


def get_register_data():  # Method to fetch the register data from the Excel sheet
    register_data = []
    # Read the Excel file into a DataFrame
    path = os.path.abspath("data/register_data.xlsx")
    df = pd.read_excel(path, 'Register')  # Update the path to your Excel file if needed

    # Iterate through the rows of the DataFrame and extract username and password
    for index, row in df.iterrows():
        first_name = row['FIRST_NAME']
        last_name = row['LAST_NAME']
        street = row['STREET']
        city = row['CITY']
        state = row['STATE']
        zipcode = row['ZIPCODE']
        phone = row['PHONE']
        ssn = row['SSN']
        username = row['USERNAME']
        password = row['PASSWORD']
        confirm_password = row['PASSWORD']
        register_data.append((first_name, last_name, street, city, state, zipcode, phone, ssn, username, password, confirm_password))

    return register_data


def update_excel(first_name, last_name, street, city, state, zipcode, phone, ssn, username, password, confirm_password, test_result, tester_name):  # Method to update the status in the Excel sheet
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    file_path = os.path.abspath("data/register_data.xlsx")
    temp_file_path = os.path.abspath("data/register_data.xlsx")

    try:
        # Load the existing Excel file into a DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return

    # Ensure necessary columns are present and of type string
    for col in ["DATE", "TIME OF TEST", "NAME OF TESTER", "TEST RESULT"]:
        if col not in df.columns:
            df[col] = ""  # Add missing columns with empty strings

    df["DATE"] = df["DATE"].astype(str)
    df["TIME OF TEST"] = df["TIME OF TEST"].astype(str)
    df["NAME OF TESTER"] = df["NAME OF TESTER"].astype(str)
    df["TEST RESULT"] = df["TEST RESULT"].astype(str)

    # Update the DataFrame with the test result for the matching username and password
    record_found = False
    for index, row in df.iterrows():
        if row["USERNAME"] == username and row["PASSWORD"] == password:
            df.at[index, "DATE"] = current_date
            df.at[index, "TIME OF TEST"] = current_time
            df.at[index, "NAME OF TESTER"] = tester_name
            df.at[index, "TEST RESULT"] = test_result
            record_found = True
            break

    if not record_found:
        print(f"No matching record found for username: {username} and password: {password}")
        return

    try:
        # Save the updated DataFrame to a temporary file
        with pd.ExcelWriter(temp_file_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Register')

        # Replace the original file with the temporary file
        os.replace(temp_file_path, file_path)
    except Exception as e:
        print(f"Error writing to the Excel file: {e}")
        # Optionally, handle the temporary file cleanup here
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@pytest.mark.usefixtures("setup")
class TestRegister:
    Error_Message = (By.XPATH, "//span[@class='error']")

    @pytest.mark.parametrize("first_name, last_name, street, city, state, zipcode, phone, ssn, username, password, confirm_password", get_register_data())
    def test_register(self, setup, first_name, last_name, street, city, state, zipcode, phone, ssn, username, password, confirm_password):
        register_page = RegisterPage(self.driver)
        register_page.register(first_name, last_name, street, city, state, zipcode, phone, ssn, username, password, confirm_password)

        # Replace 'Tester_Name' with the actual tester's name or get it dynamically
        tester_name = "Sivaramakrishnan T"

        # Check if the register was successful by verifying the presence of 'dashboard' in the URL
        if "Your account was created successfully. You are now logged in." in self.driver.page_source:
            update_excel(first_name, last_name, street, city, state, zipcode, phone, ssn, username, password, confirm_password, "Passed", tester_name)
        else:
            update_excel(first_name, last_name, street, city, state, zipcode, phone, ssn, username, password, confirm_password, "Failed", tester_name)

