#!/usr/bin/python

'''
Module to leverage CW API to interface between bot and CW
Tasks:
- Able to lookup ticket number mentioned in chat
'''

import sys

import connectpyse
from connectpyse.service import tickets_api


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


def return_sr_summary(ticket_id):
    ticket = lookup_sr(ticket_id)
    if ticket.id:
        # print(ticket)
        return '[Ticket #{}](https://na.myconnectwise.net/v4_6_release/services/system_io/Service/' \
               'fv_sr100_request.rails?service_recid={}&companyName={}): {} '.format(ticket.id, ticket.id, 'wheelhouseit', ticket.summary, )
    else:
        return 'Error: {}'.format(ticket_id)
