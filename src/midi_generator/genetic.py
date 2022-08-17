from itertools import takewhile, compress, accumulate
from typing import Tuple

from .config import Configuration, BEATS_PER_BAR
from .note import Note
from dataclasses import dataclass
import random

from .syncopation import weighted_note_to_beat, density


@dataclass
class Gene:
    pitch: int
    velocity: int
    remaining_ticks: int


@dataclass
class Individual:
    notes: list[Note]
    fitness: tuple[float]


Population = list[Individual]


def random_individual(config: Configuration):
    durations = config.rate
    start = 0
    notes = []

    while start < config.bars * BEATS_PER_BAR:
        key = random.choice(list(config.scale.notes)[30:40])
        velocity = random.randint(80, 100)
        end = min(start + random.choice(durations) * BEATS_PER_BAR, config.bars * BEATS_PER_BAR)
        notes.append(Note(key, velocity, start, end))
        start = end

    return Individual(notes, fitness(notes))


def generate_population(config: Configuration):
    return [random_individual(config) for i in range(40)]


# def mutation(individual: Individual, config: Configuration) -> Individual:
#     new_notes = []
#     for note in individual.notes:
#         change = random.random()
#         if change > 0.2:
#             new_end = min(note.start + random.choice(config.rate) * BEATS_PER_BAR, BEATS_PER_BAR * config.bars)
#             new_start = note.start
#             if len(new_notes) > 0 and not config.is_polyphonic and new_notes[-1].end > new_start:
#                 new_start = new_notes[-1].end
#             if new_start == new_end:
#                 continue
#             new_notes.append(Note(note.pitch, note.velocity, new_start, new_end))
#         else:
#             new_notes.append(Note(note.pitch, note.velocity, note.start, note.end))
#
#     return Individual(new_notes, fitness(new_notes))


def single_point_crossover(population: Population, config: Configuration) -> Population:
    max_notes = config.bars * (1 / min(config.rate)) * BEATS_PER_BAR
    for a, b in zip(population[::2], population[1::2]):
        change = random.random()
        if change > 0.4:
            cut = random.randint(0, max_notes) * min(config.rate)
            child = list(takewhile(lambda note: note.start < cut, a.notes)) + \
                list(takewhile(lambda note: note.start > cut, b.notes[::-1]))[::-1]
            population.append(Individual(child, fitness(child)))

    return population


def uniform_crossover(population: Population, config: Configuration) -> Population:
    max_notes = config.bars * (1 / min(config.rate)) * BEATS_PER_BAR
    for a, b in zip(population[::2], population[1::2]):
        change = random.random()
        if change > 0.4:
            part_a = [random.randint(0, 1)] * max_notes
            part_b = [0 if x == 1 else 1 for x in part_a]
            ...


def roulette_wheel(population: Population, config: Configuration) -> Population:
    new_population = []
    for i in range(20):
        probabilities = [0] + list(accumulate(map(lambda individual: individual.fitness, population)))
        change = random.uniform(0, probabilities[-1])
        index = len(list(takewhile(lambda x: x < change, probabilities)))
        new_population.append(population[index])

    return new_population


def individual_to_melody(individual: list[Gene]) -> list[Note]:
    notes = []
    start = 0.0
    time = 0.0
    for i, gene in enumerate(individual):
        time += 0.5
        if gene.remaining_ticks > 1:
            continue

        if gene.remaining_ticks == 1:
            notes.append(Note(gene.pitch, gene.velocity, start, time))
            start = time

        if gene.remaining_ticks == 0:
            start = time

    return notes


def fitness(genes: list[Gene]) -> tuple[float, float]:
    notes = individual_to_melody(genes)
    return abs(weighted_note_to_beat(notes) - 0.35), abs(density(genes) - 0.8)


def generator(config: Configuration):
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


def mutation(config: Configuration, genes: list[Gene]):
    for i, gene in enumerate(genes):
        change = random.random()
        if change > 0.1:
            gene.pitch = random.choice(list(config.scale.notes)[30:40])
        change = random.random()
        if change > 0.05 and gene.remaining_ticks == 1:
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
