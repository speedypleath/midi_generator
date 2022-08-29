import logging
from note import Note
from ..config import Configuration
from deap import base, creator, tools
from ..genetic import ea_simple_with_elitism, generator, fitness, melody_to_individual, mutation, check_remaining_ticks, individual_to_melody
from ..config import Configuration
import numpy as np
from midiutil import MIDIFile

Sequence = list[Note]


def generate(config: Configuration = Configuration()) -> Sequence:
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
    population = toolbox.population(100)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)
    stats.register("min_axis", np.min, axis=0)
    stats.register("avg_axis", np.mean, axis=0)

    hof = tools.HallOfFame(10)
    population, logbook = ea_simple_with_elitism(population, toolbox, cxpb=0.4, mutpb=0.2,
                                                 ngen=100, stats=stats, hall_of_fame=hof)

    hof.update(population)
    best = hof.items[0]
    logging.info('-- Best Ever Individual = %s\n', best)
    logging.info('-- Best Ever Fitness -- %s\n', best.fitness.values)
    
    melody = individual_to_melody(best)
    return melody


def mutate(sequence: Sequence, config: Configuration = Configuration()) -> Sequence:
    individual = melody_to_individual(sequence)
    mutated, = mutation(config, individual)
    return individual_to_melody(mutated)

def continue_sequence(sequence: Sequence, config: Configuration = Configuration()) -> Sequence:
    pass

def combine(sequence: Sequence, config: Configuration = Configuration()) -> Sequence:
    pass

def write_file(notes: Sequence, path: str):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)

    for note in notes:
        midi.addNote(0, 0, note.pitch, note.start, note.end - note.start, note.velocity)

    with open(f'{path}', "wb") as output_file:
        midi.writeFile(output_file)
