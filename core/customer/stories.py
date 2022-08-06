from stories import Story, I
from .models import Customer, Passport
import requests
import xml.etree.ElementTree as ET # We use this module for parsing xml data
import datetime
from dateutil.relativedelta import relativedelta


class CustomerStory(Story):
    """We use this Story to check if customer is exists or not via given pk"""

    I.check_customer_id

    def check_customer_id(self, state):
        customer = Customer.objects.filter(pk=state.pk)
        if not customer.exists():
            raise Exception("Customer not found")


class PassportStory(Story):
    """ We use thi Story extract datas from passport. We follow below sequences for it:
        1) We post to mrz_url located in .env file, then we get task ID from the response
        2) After getting task ID, we're getting task status via task status url located in .env
            file. We send task ID in data for it, and then we get result url from the response.
            Result url contains passport parameters
        3) After gettinf result url, we're sending 'GET' method to this url. Then we get passport
            data as xml format.
        4) After getting xml format we need to parsing data. After parsing we load data to the
            Passport model.
    """

    I.post_mrz_process
    I.get_task_status
    I.get_passport_data
    I.parsing_passport_data

    def post_mrz_process(self, state):
        headers = {"Authorization": f"Basic {state.token}"}
        state.headers = headers
        data = {"File": open(state.scan_file, "rb")}
        response = requests.post(url=state.mrz_url, files=data, headers=headers)
        # print(response.json())
        if response.status_code == 401:
            raise Exception("Invalid cloud token")

        state.task_id = response.json().get("taskId")
        return response.json()

    def get_task_status(self, state):
        task_url = state.task_status_url
        data = {"TaskId": state.task_id}
        response = requests.get(url=task_url, data=data, headers=state.headers)
        if response.status_code == 401:
            raise Exception("Invalid Cloud Token")
        try:
            state.result_url = response.json().get("resultUrls")[0]
        except:
            raise Exception("You have not result url to get passport data")
        return response.json()

    def get_passport_data(self, state):
        response = requests.get(url=state.result_url)
        state.xml_result = response.text # This is the xml format which contains passport datas
        return response.text

    def parsing_passport_data(self, state):
        root = ET.fromstring(state.xml_result)
        data = dict()
        for child in root:
            data[child.attrib.get("type")] = child[0].text
        passport = Passport.objects.get(id=state.passport_id)
        """ After parsing xml data, we should check if data (dict) has such keys or not,
            otherwise we will get an error.
        """
        passport.document_number = (
            data["DocumentNumber"] if "DocumentNumber" in data.keys() else ""
        )
        passport.first_name = data["GivenName"] if "GivenName" in data.keys() else ""
        passport.last_name = data["LastName"] if "LastName" in data.keys() else ""
        passport.nationality = data["Nationality"] if "Nationality" in data.keys() else ""
        if "BirthDate" in data.keys():
            birth_year = f"19{data['BirthDate'][:2]}"
            birth_month = data["BirthDate"][2:4]
            birth_day = data["BirthDate"][4:]
            birthdate_time = datetime.datetime.strptime(
                f"{birth_year}-{birth_month}-{birth_day}", "%Y-%m-%d"
            )
            passport.birth_date = birthdate_time
        passport.personal_number = (
            data["PersonalNumber"] if "PersonalNumber" in data.keys() else ""
        )
        passport.gender = data["Sex"] if data["Sex"] else ""
        if "ExpiryDate" in data.keys():
            expire_year = f"20{data['ExpiryDate'][:2]}"
            expire_month = data["ExpiryDate"][2:4]
            expire_day = data["ExpiryDate"][4:]
            expire_time = datetime.datetime.strptime(
                f"{expire_year}-{expire_month}-{expire_day}", "%Y-%m-%d"
            )
            passport.expire_date = expire_time
            issue_date = expire_time - relativedelta(years=10)
            passport.issue_date = issue_date
        passport.save()

        return data


class CheckPassportIdStory(Story):
    """ In this story we check if passport is exists or not via given pk """
   
    I.check_passport_id

    def check_passport_id(self, state):
        passport = Passport.objects.filter(pk=state.pk)
        if not passport.exists():
            raise Exception("Passport not found")

