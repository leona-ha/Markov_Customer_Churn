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

    '''
        :param states: List containing possible initial states for the simulation.
        :param p_init: List containing the probabilities of customer distribution in the first step.
        :param tmatrix: Probability Matrix for the transitions between states.
        :param index_dict: Dictionary containing state-inidices as key an states as value.
        :param state_dict: Dictionary containing states as key an state-indices as value.
        :param state: Initial customer state.
        :param history: List containing the state history of each customer.
        '''

    def transition(self):
        self.state = np.random.choice(self.states, p=self.tmatrix[self.index_dict[self.state], :])
        self.history.append(self.state)


class MarkovSimulation:

    def __init__(self, nr_steps, nr_cust,new_quote, states, p_init, tmatrix):
        self.nr_steps = nr_steps
        self.nr_cust = nr_cust
        self.new_quote = new_quote
        self.states = states
        self.p_init = p_init
        self.tmatrix = np.atleast_2d(tmatrix)
        self.index_dict = {self.states[index]: index for index in range(len(self.states))}
        self.customers = []
        self.history = pd.DataFrame()

    '''
        :param nr_steps: Nr. of steps (e.g. minutes/days...) the MarkovChain is simulated.
        :param nr_cust: Nr. of customers in the first step of the process.
        :param new_quote: Proportion of inital cust_nr added per step (e.g. 0.8).
        :param states: List containing possible initial states for the simulation.
        :param p_init: List containing the probabilities of customer distribution in the first step.
        :param tmatrix: Probability Matrix for the transitions between states.
        :param index_dict: Dictionairy mapping the possible states to an index.
        :param customers: List of Customer class instances.
        :param history: Data frame containing the purchase history of each customer.
        '''

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

    def customer_simulation(self, time_dict = False):
        if len(self.customers) == 0:
            self.create_customers()
        else:
            print("Customers have been created already")

        count = 0

        for step in range(self.nr_steps):
            count += 1

            if time_dict:
                count_index = int(count/60+7)
                new_cust = int(self.time_dict[count_index]/60)
            else:
                new_cust = int(self.nr_cust * self.new_quote)

            for cust in self.customers:
                cust.transition()

            for new_cust in range(self.new_cust):
                customer = Customer(self.states, self.p_init, self.tmatrix)
                customer.history = [None] * count + customer.history
                self.customers.append(customer)

        self.create_history()
        print('Customer flow simulation was successful')

    def __repr__(self):
        return f'''This simulation of customers in a company (e.g.supermarket) runs for {self.nr_steps} periods.
                \nIn the first step, the customer has {self.nr_cust} customers.
                \n{self.new_cust} customers are added to the market in each period.
                \nRun the simulation with the customer_simulation function'''
