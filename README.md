# winner_determination_problem
Developing a genetic algorithm that solves winner determination problems
The project is framed in the context of the winner determination problem, where the starting point is a list of bids in a multi-object auction. Each bid consists of a list of objects to be purchased, followed by the amount of money offered for those objects. The problem consists of selecting the bids in such a way as to maximize the profit, with the constraint that the same object cannot be sold twice.

To solve the problem, we have several instances of the problem in each of the .txt files, where each row represents a bid, the first value of the row is the economic amount that is offered and the rest of the elements are the objects that we want to buy with that bid.

The problem is going to be solved through the application of genetic algorithms, so we will try to obtain an optimistic solution that will not always be the optimal one. The different scripts used to solve the problem are described below:

- GA.py: implements a class containing the genetic algorithm, with different crossover operators, mutation, etc.
  
- tester.py: script to run the genetic algorithm with a given configuration of hyperparameters.
  
- Experimentation.ipynb: script that performs tests of the genetic algorithm with different instances of the problem to determine which is the best hyperparameter configuration. It incorporates the WandB optimization framework.

This project is part of the Optimization course, and the report describes the methodology and the results obtained after the completion of the project.
