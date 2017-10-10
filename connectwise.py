#!/usr/bin/python

'''
Module to leverage CW API to interface between bot and CW
Tasks:
- Able to lookup ticket number mentioned in chat
'''

import sys

from ConnectPyse.service import tickets_api
from ConnectPyse.company import companies_api, contacts_api
from ConnectPyse.system import members_api


def lookup_sr(ticket_num):
    if ticket_num.isdigit():
        try:
            ticket = tickets_api.TicketsAPI().get_ticket_by_id(ticket_num)
        except connectpyse.restapi.ApiError as err:
            ticket = 'error'
            print("API error:", err)
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return ticket
    return ''


def lookup_company(company_id):
    if company_id.isdigit():
        try:
            company = companies_api.CompaniesAPI().get_company_by_id(company_id)
        except connectpyse.restapi.ApiError as err:
            ticket = 'error'
            print("API error:", err)
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return company
    return ''


def lookup_contact(contact_id):
    if contact_id.isdigit():
        try:
            contact = contacts_api.ContactsAPI().get_contact_by_id(contact_id)
        except connectpyse.restapi.ApiError as err:
            ticket = 'error'
            print("API error:", err)
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return contact
    return ''


def get_member_by_email(email):
    # member_email = 'joshua.smith@wheelhouseit.com'
    api = members_api.MembersAPI()
    api.conditions = 'officeEmail="{}"'.format(email)
    member = next(api.get_members())
    # print(member.identifier)
    return member


def return_sr_summary(ticket_id):
    ticket = lookup_sr(ticket_id)
    if ticket.id:
        return '[Ticket #{}](https://na.myconnectwise.net/v4_6_release/services/system_io/Service/' \
               'fv_sr100_request.rails?service_recid={}&companyName={}): {}' \
               ' <br>{}/{} '.\
            format(ticket.id, ticket.id, 'wheelhouseit', ticket.summary, ticket.company['name'], ticket.contact['name'])
    else:
        return 'Error: {}'.format(ticket_id)
