from itertools import takewhile

from .config import Configuration
from dataclasses import dataclass
import random
from deap import base, creator, algorithms, tools


from src.midi_generator.syncopation import weighted_note_to_beat, density

from note import Note


@dataclass
class Gene:
    pitch: int
    velocity: int
    remaining_ticks: int


def individual_to_melody(individual: list[Gene]) -> list[Note]:
    notes = []
    start = 0.0
    time = 0.0
    for i, gene in enumerate(individual):
        time += 0.5

        if gene.remaining_ticks >= 1:
            continue

        notes.append(Note(gene.pitch, gene.velocity, start, time))
        start = time

    return notes


def melody_to_individual(melody: list[Note]) -> list[Gene]:
    genes = [Gene(0, 0, 0)] * 32
    for note in melody:
        ticks = int((note.end - note.start) * 2)
        for i in range(ticks - 1, -1, -1):
            genes[int(note.start * 2 + ticks - i - 1)] = Gene(note.pitch, note.velocity, i)
    assert(len(genes) > 0)
    return genes


def fitness(genes: list[Gene]) -> tuple[float, float]:
    notes = individual_to_melody(genes)
    return abs(weighted_note_to_beat(notes) - 0.35), abs(density(genes) - 0.8)


def generator(config: Configuration = Configuration()):
    prev_gene: Gene | None = None

    def create_random_gene() -> Gene:
        nonlocal prev_gene
        if prev_gene is not None and prev_gene.remaining_ticks > 1:
            prev_gene = Gene(prev_gene.pitch, prev_gene.velocity, prev_gene.remaining_ticks - 1)
            return prev_gene

        tick = min(config.rate)
        duration = int(random.choice(config.rate) / tick)
        key = random.choice(list(config.scale.notes)[30:40])
        velocity = random.randint(80, 100)
        prev_gene = Gene(key, velocity, duration)
        return prev_gene

    return create_random_gene


def mutation(config: Configuration, genes):
    for gene in genes:
        change = random.random()
        if change > 0.9:
            gene.pitch = random.choice(list(config.scale.notes)[30:40])
        change = random.random()
        if change > 0.9 and gene.remaining_ticks == 1:
            gene.remaining_ticks = 0
    return genes,


def check_remaining_ticks():
    def decorator(func):
        def wrapper(*args, **kwargs):
            offspring = func(*args, **kwargs)
            for genes in offspring:
                for i, gene in enumerate(genes):
                    if gene.remaining_ticks == 0:
                        continue
                    gene.remaining_ticks = len(list(takewhile(lambda x: x.pitch == gene.pitch, genes[i:])))
            return offspring

        return wrapper

    return decorator


def ea_simple_with_elitism(population, toolbox, cxpb, mutpb, ngen, stats=None,
                           hall_of_fame=None, verbose=False):
    """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that
    halloffame is used to implement an elitism mechanism. The individuals contained in the
    halloffame are directly injected into the next generation and are not subject to the
    genetic operators of selection, crossover and mutation.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if hall_of_fame is None:
        raise ValueError("halloffame parameter must not be empty!")

    hall_of_fame.update(population)
    hof_size = len(hall_of_fame.items) if hall_of_fame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population) - hof_size)

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # add the best back to population:
        offspring.extend(hall_of_fame.items)

        # Update the hall of fame with the generated individuals
        hall_of_fame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook


def create_config(config):
    toolbox = base.Toolbox()
    creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
    toolbox.register("generator", generator())
    creator.create("Individual", list, fitness=creator.Fitness)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.generator, n=32)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness)
    toolbox.register("select", tools.selStochasticUniversalSampling)
    toolbox.register("mutate", mutation, config)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("select", tools.selTournament, tournsize=3)
    decorator = check_remaining_ticks()
    toolbox.decorate("mate", decorator)
    toolbox.decorate("mutate", decorator)
    return toolbox
