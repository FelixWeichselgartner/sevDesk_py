"""
https://my.sevdesk.de/swaggerUI/index.html
https://my.sevdesk.de/swaggerJSON/swagger.json
"""


import requests
import json


def get_phone_mail_from_communications(communications, customer_id):
    phone = None
    mail = None
    more_data = None
    for c in communications:
        if c['contact']['id'] == customer_id:
            if c['key']['id'] == '2':
                
                if c['type'] == 'PHONE':
                    phone = c['value']
                elif c['type'] == 'EMAIL':
                    mail = c['value']
            more_data = c
    if phone != None:
        if phone[3] != '1':
            # TODO: more info here on customer number or name.
            print(f'please check the customer with number {phone}, {mail}')
            print(more_data)
            print('this does not seem like a phone number to me')
    return phone, mail


class sevDesk:

    def __init__(self, email, token):
        self.base_url = 'https://my.sevdesk.de/api/v1/'
        self.email = email
        self.token = token
        self.headers = {'Authorization': self.token}

    """
    doc: https://my.sevdesk.de/swaggerUI/index.html#/Contact/getContacts
    """
    def get_contacts(self, depth=1, limit=9999, offset=0):
        url = self.base_url + f'Contact/?depth={depth}&limit={limit}&offset={offset}'
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.content)
        return data['objects']

    def get_contact_address(self, id_contact):
        url = self.base_url + f'Contact/{id_contact}/getAddresses'
        response = requests.get(url, headers=self.headers)
        # print(response)
        data = json.loads(response.content)
        # print(data)
        return data['objects']

    def get_contact_mail(self, id_contact):
        print('get_contact_mail is deprecated for get_communication_ways')
        url = self.base_url + f'Contact/{id_contact}/getMainEmail'
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.content)
        _mail = data['objects']
        if _mail != None:
            return _mail['value']
        else:
            return None

    def get_communication_ways(self, limit=9999):
        url = self.base_url + f'CommunicationWay/?limit={limit}'
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.content)
        return data['objects']

    def get_contact_phone(self, id_contact):
        print('get_contact_phone is deprecated for get_communication_ways')
        url = self.base_url + f'Contact/{id_contact}/getMainPhone'
        response = requests.get(url, headers=self.headers)
        print(response.content)
        data = json.loads(response.content)
        _phone = data['objects']
        if _phone != None:
            return _phone['value']
        else:
            return None

    """
    doc: https://my.sevdesk.de/swaggerUI/index.html#/Contact/addContact
    """
    def add_contact_person(self, name, customerNumber, gender, firstname, description):
        url = self.base_url + "Contact/"

        data = {
            'category[id]': 3,
            'category[objectName]': 'Category',
            'familyname': name,
            'customerNumber': customerNumber,
            'gender': gender,
            'surename': firstname,
            'description': description
        }

        response = requests.post(url, data=data, headers=self.headers)
        ret = json.loads(response.content)

        return ret['objects']['id']

    def add_contact_phone(self, id_contact, phone):
        url = self.base_url + f"Contact/{id_contact}/addPhone"

        data = {
            'key': 1,
            'value': phone
        }

        response = requests.post(url, data=data, headers=self.headers)

    def add_contact_email(self, id_contact, email):
        url = self.base_url + f"Contact/{id_contact}/addEmail"

        data = {
            'key': 1,
            'value': email
        }

        response = requests.post(url, data=data, headers=self.headers)

    def add_contact_address(self, id_contact, street, zip, city):
        url = self.base_url + f"Contact/{id_contact}/addAddress"

        data = {
            'street': street,
            'zip': zip,
            'city': city,
            'country': '1'  # 1 == Germany
        }

        response = requests.post(url, data=data, headers=self.headers)
