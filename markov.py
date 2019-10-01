""" Define MarkovChain class to simulate Customer Churn """
import numpy as np
import pandas as pd

class MarkovChain:
    """ Simulate future states with transition probabilities """
    def __init__(self, tmatrix, states):
        """
        Initialize MarkovChain instance
        Parameters:
        1. transition_matrix= at least 2d matrix with probabilities
        2. states= list of possible states. Must be same order as in matrix
        3. index_dict= assigns an index to each state
        """
        self.tmatrix = np.atleast_2d(tmatrix)
        self.states = states
        self.index_dict = {self.states[index]: index for index in range(len(self.states))}

    def next_state(self, current_state):
        """ Predicts future state based on initial state"""
        return np.random.choice(self.states, p=self.tmatrix[self.index_dict[current_state], :])

    def generate_states(self, current_state, step_nr):
        """ Creates list of future states based on initial state"""
        future_states = []
        for i in range(step_nr):
            next_state = self.next_state(current_state)
            future_states.append(next_state)
            current_state = next_state
        return future_states

    def cust_nr(self, state_list, step_nr, new_quote= 0.75):
        """
        Simulate number of subjects in different states after certain timesteps. Returns dataframe.
        Arguments:
        - state_list: list or series containing the amount of subjects per state. Must be same order as "states"
        - step_nr: number of timesteps
        - new_quote: amount of new subjects added per timestep (e.g. 0.75 leads to 0.75* initial number of subjects)
        """
        init_state = np.array(state_list)
        state_a, state_b, state_c, state_d, state_e = [init_state[0]], [init_state[1]], [init_state[2]], [init_state[3]], []
        for i in range(1,step_nr):
            new_cust=list((np.random.dirichlet(np.ones(4))*(state_list.sum()*new_quote)).astype(int))
            new_cust=np.append(new_cust,0)
            state_a.append(init_state[0]+new_cust[0])
            state_b.append(init_state[1]+new_cust[1])
            state_c.append(init_state[2]+new_cust[2])
            state_d.append(init_state[3]+new_cust[3])
            state_e.append(init_state[4])
            init_state = (init_state+new_cust).dot(self.tmatrix)
        clf = pd.DataFrame(zip(state_a, state_b, state_c, state_d, state_e), columns=self.states)

        return clf

    def cust_nr_checkout(self, state_list, step_nr, new_quote):
        """
        Simulate number of subjects in different states after certain timesteps.
        If no "death-end" (e.g. "churned customer") exits use cust_nr function.
        Returns a dataframe with length step_nr.
        Arguments:
        - state_list: list or series containing the amount of subjects per state.
            Must be same order as "states"
        - step_nr: number of timesteps
        - new_quote: amount of new subjects added per timestep
            (e.g. 0.75 leads to 0.75* initial number of subjects.
            If no new subjects should be added set new_quote=0)
        """
        init_state = np.array(state_list)
        state_set = [[i] for i in state_list[:-1]] + [[]]

        for i in range(1, step_nr):
            new_cust = list((np.random.dirichlet(np.ones(len(state_list)-1)) * (state_list.sum() * new_quote)).astype(int))
            new_cust = np.append(new_cust, 0)
            for j in range(len(state_list)-1):
                state_set[j].append(init_state[j] + new_cust[j])
            state_set[-1].append(init_state[-1])
            init_state[-1] = 0
            init_state = (init_state + new_cust).dot(self.tmatrix)
        state_set[-1].append(init_state[-1])
        csm = pd.DataFrame(state_set).T.astype(int)
        csm.columns = self.states

        return csm

    def get_clv(self, market, price_df, state_list, step_nr, death_end = False):
        """
        Simulate customer lifetime value (clv).
        Arguments:
        - market: market name. Should be the same as in price_df
        - price_df: dataframe containing prices per market and item
        - state_list: list or series containing the amount of subjects per state
        - death_end: does the simulation contain a death end (e.g. churned customer)
        -
        """
        pricelist = list(price_df.loc[market])
        if death_end:
            df= self.cust_nr_churned(state_list, step_nr)
        else:
            df = self.cust_nr(state_list, step_nr)

        return pricelist*df
