import os
import math
import json
import requests
import unittest

#vars
url = "https://zcc-sgannon.zendesk.com/api/v2/tickets.json"
user = "spencer.gannon@valpo.edu/token"
token = "S2KahNtHlAHkfwZttxaOY8xXTfZoRVrszTctizvh"
current_tickets = []    #list of tickets that have yet to be solved or are in progress
menu_input = 0

#functions
clear = lambda: os.system("cls")    #clears console

#created class in order to unit test functions
class Tickets():
    tickets = []

    def print_ticket(self, ticket):
        try:
            print("|{:^9d}|{:13d}|{:29s}{:3s}|{:30s}...|{:22s}|".format(ticket["id"],
                                                                        ticket["requester_id"],
                                                                        ticket["subject"][0:(29 if len(ticket["subject"]) > 29 else len(ticket["subject"]))],
                                                                        "..." if len(ticket["subject"]) > 29 else "",
                                                                        ticket["description"].replace("\n","")[0:30], ticket["created_at"]))
        except:
            print(f"Error: ticket has invalid format.\nTicket: {ticket}")
            return None

    def print_ticket_at_index(self, index):
        try:
            self.print_ticket(self.tickets[index])
        except IndexError:
            print(f"Error: index {index} does not exist")
            return None

    def print_multiple_tickets(self):
        table_header = "|{:^9s}|{:^13s}|{:^32s}|{:^33s}|{:^22s}|".format("Ticket ID","Requester ID","Subject","Description","Created at")
        line = "-"*len(table_header)

        print("%s\n%s\n%s" % (line, table_header, line))
        for ticket in self.tickets:
            self.print_ticket(ticket)
        print(line)

    def set_tickets(self):
        response = requests.get(url, auth=(user, token))
        self.tickets = response.json()["tickets"]
        if response.status_code != 200:
            print(f"Status code: {response.status_code}. Error! Exiting...")
            return False
        else:
            return True

    def get_ticket_at_index(self, index):
        try:
            return self.tickets[index]
        except IndexError:
            print(f"Error: index {index} does not exist")
            return None

    def get_tickets(self):
        return self.tickets

    def get_length(self):
        return len(self.tickets)

if __name__ == "__main__":
    tickets = Tickets()

    if not tickets.set_tickets():   #if it returns false, the API is down/unavailable
        print("API is currently unavailable! Please try again later!\n")
        input("Hit enter to end the program...")
        exit()

    while menu_input != 4:
        print("\t\tWelcome to the Zendesk Ticket Viewer!\n")
        print("\t1. View all tickets\n\t2. View a single ticket\n\t3. Update active tickets\n\t4. Exit\n")
        menu_input = int(input("Enter a number >> "));
        if menu_input == 1:     #view all tickets
            clear()
            if tickets.get_length() > 25:
                page_input = 0
                while page_input != -2:
                    clear()
                    print(f"Page {page_input + 1}")
                    for i in range(25 * page_input, (25 * page_input) + 25):
                        tickets.print_ticket_at_index(i)
                    page_input = int(input("Enter in another page number or -1 to exit >> ")) - 1
                    while not (page_input == -2 or (page_input >= 0 and page_input <= round(tickets.get_length()/25) - 1)):
                        clear()
                        print(f"Error. Page number {page_input + 1} does not exist.\n")
                        page_input = int(input("Enter in another page number or -1 to exit >> ")) - 1
            else:
                tickets.print_multiple_tickets()
                input("\nHit enter to return to the menu")
        elif menu_input == 2:   #view a single ticket
            clear()
            if tickets.get_length() > 0:
                ticket = None
                while ticket is None:
                    last_id = tickets.get_ticket_at_index(-1)["id"]
                    search_id = int(input(f"Enter a ticket id (1 - {last_id})>> "))
                    for t in tickets.get_tickets():
                        if t["id"] == search_id:
                            ticket = t
                            break
                    if ticket is None:
                        print(f"Ticket with ID {search_id} does not exist or is closed.")
                clear()
                tickets.print_ticket(ticket)
                input("\nHit enter to return to the menu")
            else:
                input("There are currently no tickets! Hit enter to go back to the menu")
        elif menu_input == 3:
            tickets.set_tickets()
