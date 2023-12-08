# -*- coding: utf-8 -*-


import random
import numpy as np
import copy
import time

class GA: #class implementing the genetic algorithm

    def read_problem_instance(self,problem_path): #read the text file and save the number of goods, number of bids
        
        #and for each bid its bid (float) and the goods it bids for (set class)
        """
        TODO: Implementar método para leer una instancia del problema
        y ajustar los atributos internos del objeto necesarios
        """
        apuestas=[]
        with open(problem_path,'r') as file:
            
            for linea in file:
                lista=linea.split()
                if len(lista)>0:
                    if lista[0]=='goods':

                        bienes=int(lista[1])

                    elif lista[0]=='bids':

                        n_apuestas=int(lista[1])

                    else:
                        
                        apuestas.append((float(lista[1]),set(lista[2:-1])))
        
        return bienes, n_apuestas, apuestas
    
    def create_random_solution(self): #creates a list of length self.n_apuestas, consisting of random numbers between 0 and 1
        
        return [random.random() for i in range(self.n_apuestas)]

    def create_ponderate_solution(self): #creates a list of length self.n_apuestas, consisting of random numbers between 0 and 1
        
        return [random.random()*len(self.apuestas[i][1])/self.apuestas[i][0] for i in range(self.n_apuestas)]
    
    def create_random_population(self): #creates a list of solutions, as many solutions as the attribute self.tamano_poblacion_inicial

        return [self.create_random_solution() for i in range(self.tamano_poblacion_inicial)] if self.sol=='simple' else [self.create_ponderate_solution() for i in range(self.tamano_poblacion_inicial)]
    
    def get_fitness(self, solucion): #calculates only the score of the individual passed by parameter

        
        vendidos=set() #set that stores the goods we have already sold
        fitness=0 #accumulated score
        
        for i in np.argsort(solucion): #we scroll through the individual's positions from the lowest to the highest random number
            
            ap=self.apuestas[i] #we keep the bet

            if len(vendidos.intersection(ap[1]))==0: # if the items of that bid have not yet been sold
                
                #we accept bid
                fitness+=ap[0] #update accumulated score
                vendidos=vendidos.union(ap[1]) #we add the items we have just sold to the set of all items sold
                
            
        return fitness #return the score
        
    
    def get_fitness_and_vec(self, solucion): #calculates the score and the representation of the individual passed by parameter        
        #same implementation as the previous method, but in addition to the score, it returns a vector with the representation of the individual
        
        
        vendidos=set()
        fitness=0 
        vector_binario=[] #vector we use for the representation
        
        for i in np.argsort(solucion): 
            
            ap=self.apuestas[i] 

            if len(vendidos.intersection(ap[1]))==0: #
                
                
                fitness+=ap[0] 
                vendidos=vendidos.union(ap[1]) 
                vector_binario.append(i)  #we add the stake we have accepted to the representation vector
            
        return fitness,vector_binario #we return both score and representation vector
                    
    def get_best_solution(self): #displays the score of the best solution and returns a vector of accepted bets
        """
        Método para devolver la mejor solución encontrada hasta
        el momento
        """
        #TODO
        print('Mejor fitness encontrado: ', self.best_solution)
        return self.solution_vector
    
################################################################################    
################# CROSSOVER AND MUTATION OPERATORS EXPLAINED ###################
################################################################################

    #SIMPLE SWAP
    def simple_swap(self,individual):
      #TODO
        hijo=copy.copy(individual)
        p1=random.randint(0,len(individual)-2) #we select a random position
        p2=random.randint(p1,len(individual)-1) #select the second position
        hijo[p1],hijo[p2]=hijo[p2],hijo[p1] #we swap their values
        return hijo
    #HIGH-LOW SWAP
    def high_low_swap(self,individual):
        hijo=copy.copy(individual)
        m = len(hijo)//2
        indexes = np.argsort(hijo)
        p1, p2 = random.choice(indexes[:m]), random.choice(indexes[m:]) #one index is selected with a low and one with a high value
        hijo[p1],hijo[p2]=hijo[p2],hijo[p1] #we swap their values
        return hijo
    
    #BIASED CROSSOVER
    def cruce_sesgado(self,individual1, individual2,p_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE REST OF THE POPULATION.

        hijo = []
        
        for i in range(len(individual1)): #for each gene on the chromosome
            
            p=random.random()
            
            if p<p_elite: #with probability p_elite inherits the gene from the father of the elite population
                
                hijo.append(individual1[i])
            else: #with probability 1-p_elite inherits the gene from the parent of the subelite population
                hijo.append(individual2[i])
        
        
        return hijo

    #COMPLETE ARITHMETIC COMBINATION

    def cruce_recombinacion_arit_completa(self, individual1, individual2, p_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE REST OF THE POPULATION.

      hijo = []

      for i in range(len(individual1)): #for each gene on the chromosome

        hijo[i]= p_elite*individual1[i]+(1-p_elite)*individual2[i] #The average of this index of the parents is taken, 
                                                                  #giving more weight to the individual from the elite population.
      
      return hijo

      #SIMPLE ARITHMETIC COMBINATION

    def aritmetica_simple(self, individual1, individual2, prob_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE REST OF THE POPULATION.
    
      hijo = []
      p_corte = random.randint(1,len(individual1)-1) #we select a gene of the chromosome
      hijo = individual1[0:p_corte] #the above genes are inherited from the father of the elite population.
      
      for i in range (p_corte, len(individual1)): #all other genes are inherited by making 
                                                #the p_elite weighted mean of both parents
          hijo.append(prob_elite*individual1[i] + (1-prob_elite)*individual2[i])
          
      return hijo

    
      #UNIQUE ARITHMETIC COMBINATION
    def aritmetica_unica(self, individual1, individual2, prob_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE REST OF THE POPULATION.
        
        hijo = copy.copy(individual1) #the whole chromosome is inherited from the elite parent except for one point
        p_corte = random.randint(1,len(individual1)-1) #we select a gene of the chromosome
        #calculate the p_elite weighted mean of that gene for both parents
        hijo[p_corte] = prob_elite*individual1[p_corte] + (1-prob_elite)*individual2[p_corte]
                                
        return hijo

    
    
###############################################################################
###############################################################################
###############################################################################


    def select_best_n(self,population, n): #Selects the best N solutions of a population

        #returns a list of the N best solutions and another list of the remaining solutions
        sorted_population= sorted(population,key= lambda sol: self.get_fitness(sol),reverse=True)
        return sorted_population[:n], sorted_population[n:]


    def run(self):
        """
        Método que ejecuta el algoritmo genético. Debe crear la población inicial y
        ejecutar el bucle principal del algoritmo genético
        TODO: Se debe implementar aquí la lógica del algoritmo genético
        """
        time_ini = time.time() #we initialize time
        
        generaciones_cambiando=0
        
        time_fin =time.time()
      
            
        poblacion = self.create_random_population() #we create initial population
            
        while generaciones_cambiando < 100 and time_fin-time_ini<self.time_deadline: #If we have not improved the solution for 100 generations or if the time limit is exceeded, the algorithm terminates.
                
              p_elite, p_sub_elite = self.select_best_n(poblacion, self.tamano_elite) #we divide the population between elite and sub-elite solutions.

              next_poblacion = copy.copy(p_elite) #elite indiviudals are directly passed to the next generation
                
              n_mutantes = random.randint(1,self.tamano_poblacion_inicial//2) #we add to the next generation random solutions (between 1 and initial_population_size/2)
              #the type of solutions to be added is determined by the parameter self.sol
              if self.sol =='simple':
                for i in range(n_mutantes):

                    next_poblacion.append(self.create_random_solution())
              else:
                  for i in range(n_mutantes):

                    next_poblacion.append(self.create_ponderate_solution())


            #to complete the size of the population of the next generation
              for i in range(self.tamano_poblacion_inicial-len(next_poblacion)): #we apply crossover operators

                  p1 = random.choice(p_elite) #we chose parent from the elite population

                  if self.operador_seleccion=='completa':
                    p2 = random.choice(poblacion) #we select father of the whole population
                  
                  elif self.operador_seleccion=='subelite':
                    p2 = random.choice(p_sub_elite) #we select father of the subelite population
                  
                  else:

                    print('Error,operador de selección no válido')
                    break
                #we apply a crossover operator (self.operador_cruce)
                  if self.operador_cruce == 'sesgado':
                    hijo = self.cruce_sesgado(p1,p2,self.p_elite) 

                  elif self.operador_cruce == 'ac':
                    hijo = self.cruce_recombinacion_arit_completa(p1,p2,self.p_elite)

                  elif self.operador_cruce == 'as':
                    hijo = self.aritmetica_simple(p1,p2,self.p_elite)
                  
                  elif self.operador_cruce == 'au':
                    hijo = self.aritmetica_unica(p1,p2,self.p_elite)

                  else:
                    print('Error, operador de cruce no válido')
                    break
                    
                  if random.random()<self.p_mutacion: #with probability p_mutation the child mutates
                      
                      if self.operador_mutacion=='simple':
                        hijo = self.simple_swap(hijo)
                      elif self.operador_mutacion=='hl':
                        hijo = self.high_low_swap(hijo)
                      else:
                        print('Error, operador de mutación no válido')
                        break
                        
                  next_poblacion.append(hijo) #we add child to the next generation population.

              poblacion= copy.copy(next_poblacion) #we update the new population

              mejor, resto = self.select_best_n(poblacion, 1) #evaluate the best solution of this generation
                
              punt, rpr = self.get_fitness_and_vec(mejor[0]) #get its score and representation
                
              if punt > self.best_solution: #if it improves on the best solution obtained so far
                  self.tiempo_mejor_sol=time.time()-time_ini
                  self.best_solution=punt #we update the best solution obtained
                  self.solution_vector=rpr
                  generaciones_cambiando=0 #we reset the counter of generations without improving the solution
              else: #if it does not improve
                  generaciones_cambiando+=1 #updating the generation counter without improving the solution

              time_fin=time.time()      

            

    def __init__(self,time_deadline=180,problem_path='hard-0.txt',tamano_poblacion_inicial=150,operador_cruce='sesgado', p_elite=0.8, 
                 operador_mutacion='simple',p_mutacion=0.15, operador_seleccion='subelite', tamano_elite=0.25, sol='ponderada'):
        
        """
        Inicializador de los objetos de la clase. Usar
        este método para hacer todo el trabajo previo y necesario
        para configurar el algoritmo genético
        Args:
            problem_path: Cadena de texto que determina la ruta en la que se encuentra la definición del problema
            time_deadline: Límite de tiempo que el algoritmo genético puede computar
        """

        self.tamano_poblacion_inicial=tamano_poblacion_inicial #number of random sols to start the alg with
        
        self.n_bienes,self.n_apuestas,self.apuestas=self.read_problem_instance(problem_path) #number of goods to be auctioned
        
        self.best_solution = 0 #Attribute to store the value of the best solution found.
        
        self.solution_vector = None #Attribute to store the representation of the best solution found so far.
        
        self.tiempo_mejor_sol = None #Attribute to store the time it takes to find the best solution
        
        self.time_deadline = time_deadline # Time limit (in seconds) for the computation of the genetic algorithm
        
        self.operador_cruce = operador_cruce #crossover operator used in the genetic
        
        self.p_elite = p_elite #probability of obtaining genetic material from the elite parent
        
        self.operador_mutacion = operador_mutacion #mutation operator
        
        self.p_mutacion = p_mutacion #probability of mutation
        
        self.operador_seleccion = operador_seleccion #parent selection operator used in the genetic

        self.tamano_elite = int(round(tamano_poblacion_inicial*tamano_elite,0))

        self.sol = sol #whether the solutions generated are completely random or weighted






########################################################################
########################################################################
###### IMPLEMENTED OPERATORS (AS FUNCTIONS OUTSIDE THE CLASS) ##########
########################################################################
########################################################################

# ### Mutation operators (minimum 2)

#simple swap
def simple_swap(individual):
    hijo=copy.copy(individual)
    p1=random.randint(0,len(individual)-2) #se selecciona una posición del cromosoma
    p2=random.randint(p1,len(individual)-1) #se selecciona otra posición del cromosoma
    hijo[p1],hijo[p2]=hijo[p2],hijo[p1] #se intercambian sus valores
    return hijo

#high-low swap
def high_low_swap(individual):
    hijo=copy.copy(individual)
    m = len(hijo)//2
    indexes = np.argsort(hijo)
    p1, p2 = random.choice(indexes[:m]), random.choice(indexes[m:]) #se selecciona un valor bajo y otro alto
    hijo[p1],hijo[p2]=hijo[p2],hijo[p1] #se intercambian sus valores
    return hijo


# ### Crossover operators (minimum 3)

# BIASED CURRENCY OPERATOR

def cruce_sesgado(self,individual1, individual2, p_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE WHOLE POPULATION.

    hijo = []
        
    for i in range(len(individual1)): #PARA CADA GEN DEL CROMOSOMA HIJO
            
        p=random.random()
            
        if p<0.75: #CON 75% DE PROB HEREDA DEL INDIVIDUO ELITE
                
            hijo.append(individual1[i])
        else: #CON UN 25 DE PROB HEREDA DEL INDIVIDUO SUB-ELITE
            hijo.append(individual2[i])
        
        
    return hijo

#COMPLETE ARITHMETIC COMBINATION

def cruce_recombinacion_arit_completa(self, individual1, individual2, p_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE WHOLE POPULATION.

  hijo = []

  for i in range(len(individual1)): #para cada índice

    hijo[i]= p_elite*individual1[i]+(1-p_elite)*individual2[i] #se realiza la media de ese índice de los padres, 
                                                              #dando más peso al individuo de la población de élite
  
  return hijo

#SIMPLE ARITHMETIC COMBINATION

def aritmetica_simple(self, individual1, individual2, prob_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE WHOLE POPULATION.
    
    hijo = []
    p_corte = random.randint(1,len(individual1)-1)
    hijo = individual1[0:p_corte]
    
    for i in range (p_corte, len(individual1)):
        hijo.append(prob_elite*individual1[i] + (1-prob_elite)*individual2[i])
        
    return hijo


#SINGLE ARITHMETIC COMBINATION

def aritmetica_unica(self, individual1, individual2, prob_elite): #INDIVIDUAL 1 BELONGS TO THE ELITE POPULATION, INDIVIDUAL 2 TO THE WHOLE POPULATION.
    
    hijo = copy.copy(individual1)
    p_corte = random.randint(1,len(individual1)-1)
    
    hijo[p_corte] = prob_elite*individual1[p_corte] + (1-prob_elite)*individual2[p_corte]
                             
    return hijo


# ### Parent selection operators (minimum 1)

#Option 1: 1 parent elite population and 1 parent subelite population

### Option 2: 1 parent elite population and 1 parent whole population

### Replacement operators (at least 1)

#Implicitly made, explained in the report


