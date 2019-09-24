# Markov_Customer_Churn
This project aims to model the churn of customers in a exemplary supermarket via a Markov Chain.
Markov Chains are relatively simple models of state-to-state transitions that fulfill the Markov Property - this means, that the next state of a process depends only upon the present state and not on the events that preceded it. They are used in a wide range of applications like speech recognition, bioinformatics, economics etc. .

To fulfill the Markov Property in a first-order Markov Chain, the following assumptions must be met:
1. There is a finite set of states
2. The probabilities of moving between states are fixed and don't change over time (this assumption is a major drawback of Markov Chains)
3. State accessibility (= you can move from every segment to a different segment without external restriction)
4. Non cyclic transitions


In the following example, I will model the movement of customers in the "DOODL" supermarket following the questions formulated in the document Supermarket.pdf .
The different sections in the supermarked add up to 5 possible states:
1. drinks
2. dairy
3. spices
4. fruits
5. checkout

The .csv files contain data about the movement of customers in the supermarket from Monday to Friday. 
