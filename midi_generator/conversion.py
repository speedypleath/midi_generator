from functools import reduce

from note import Note, Configuration
from .types import Gene


def individual_to_melody(individual: list[Gene], config: Configuration) -> list[Note]:
    notes = []
    start = 0.0
    time = 0.0
    for i, gene in enumerate(individual):
        time += config.tempo * config.rate / 60 * 2

        if gene.remaining_ticks > 1:
            continue

        if gene.remaining_ticks != 0:
            notes.append(Note(int(gene.pitch), int(gene.velocity), start, time))
        start = time

    return notes


def melody_to_individual(melody: list[Note], config: Configuration) -> list[Gene]:
    genes = [Gene(0, 0, 0)] * config.bars * int(1 / config.rate)
    for note in melody:
        ticks = int((note.end - note.start) * (1 / config.rate) / config.bars) + 1
        for i in range(ticks, 0, -1):
            genes[int(note.start * 2 + ticks - i - 1)] = Gene(note.pitch, note.velocity, i)

    return genes


def encodable(notes: list[Gene]) -> str:
    return reduce(lambda x, y: x + ',' + y, [str(note.pitch) for note in notes])
