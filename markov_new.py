""" Define a Customer and a Simulation class to simulate Customer Behaviour """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Customer:
    def __init__(self, states, p_init, tmatrix):

        self.states = states
        self.p_init = p_init
        self.tmatrix = np.atleast_2d(tmatrix)
        self.index_dict = {self.states[index]: index for index in range(len(self.states))}
        self.state_dict = {index: self.states[index] for index in range(len(self.states))}
        self.state = self.state_dict[np.random.choice((len(self.states)-1),p=self.p_init,size=1)[0]]
        self.history = [self.state]

    def transition(self):
        self.state = np.random.choice(self.states, p=self.tmatrix[self.index_dict[self.state], :])
        self.history.append(self.state)


class MarkovSimulation:

    def __init__(self, nr_steps, nr_cust,new_quote, states, p_init, tmatrix):
        self.nr_steps = nr_steps
        self.nr_cust = nr_cust
        self.new_cust = int(nr_cust * new_quote)
        self.states = states
        self.p_init = p_init
        self.tmatrix = np.atleast_2d(tmatrix)
        self.index_dict = {self.states[index]: index for index in range(len(self.states))}
        self.customers = []
        self.history = pd.DataFrame()

    def create_customers(self):
        for step in range(self.nr_cust):
            customer = Customer(self.states, self.p_init, self.tmatrix)
            self.customers.append(customer)

    def one_transition(self):
        for cust in self.customers:
            cust.transition()

    def create_history(self):
        for cust in self.customers:
            self.history = pd.concat([self.history, pd.DataFrame(cust.history)], axis=1)

        self.history = self.history.T.reset_index(drop=True)
        self.history.index.name = 'customer_id'

    def customer_simulation(self):
        if len(customers) == 0:
            self.create_customers()
        else:
            print("Customers have been created already")

        count = 0

        for step in range(self.nr_steps):
            count += 1

            for cust in self.customers:
                cust.transition()

            for new_cust in range(self.new_cust):
                customer = Customer(self.states, self.p_init, self.tmatrix)
                customer.history = [None] * count + customer.history
                self.customers.append(customer)

        self.create_history()
        print('Customer flow simulation was successful')
