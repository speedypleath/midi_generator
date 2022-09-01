from note import Note
from src.midi_generator.genetic import Gene


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


def encodable(notes: list[Gene]) -> list:
    return [note.pitch for note in notes]
