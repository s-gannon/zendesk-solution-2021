import unittest
from zendesk_solution_gannon import Tickets

class TestTicketFunctions(unittest.TestCase):
    def test_get_tickets(self):
        ticket = Tickets()
        self.assertEqual(None, ticket.print_ticket({}))

    def test_init(self):
        ticket = Tickets()
        self.assertEqual([], ticket.get_tickets())

    def test_get_ticket_at_index(self):
        ticket = Tickets()
        self.assertEqual(None, ticket.get_ticket_at_index(0))

    def test_get_length(self):
        ticket = Tickets()
        self.assertEqual(0, ticket.get_length())

if __name__ == "__main__":
    unittest.main()
