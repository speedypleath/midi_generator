from deap import creator, base

creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0, -1.0))
creator.create("KolmogorovFitness", base.Fitness, weights=(1.0,))

creator.create("Individual", list, fitness=creator.Fitness)
creator.create("KolmogorovIndividual", list, fitness=creator.KolmogorovFitness)
