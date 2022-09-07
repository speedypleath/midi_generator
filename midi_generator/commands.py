from note import Note, Configuration

from .conversion import encodable, melody_to_individual
from .genetic import individual_to_melody, create_config, run_genetic_algorithm
from midiutil import MIDIFile

Sequence = list[Note]


def generate(config=Configuration()) -> Sequence:
    return run_genetic_algorithm(config)


def mutate(sequence: Sequence, config=Configuration()) -> Sequence:
    individual = melody_to_individual(sequence, config)
    toolbox = create_config(config)

    mutant = toolbox.clone(individual)
    ind, = toolbox.mutate(mutant)
    melody = individual_to_melody(ind, config)
    return melody


def continue_sequence(sequence: Sequence, config=Configuration()) -> Sequence:
    config.match = [encodable(melody_to_individual(sequence, config))]
    config.fitness_method = 'kolmogorov'

    return run_genetic_algorithm(config)


def combine(sequences: list[Sequence], config: Configuration = Configuration()) -> Sequence:
    config.match = [encodable(melody_to_individual(sequence, config)) for sequence in sequences]
    config.fitness_method = 'kolmogorov'
    return run_genetic_algorithm(config)


def write_file(notes: Sequence, path: str):
    midi = MIDIFile(1, file_format=2)
    midi.addTempo(0, 0, 120)

    for note in notes:
        midi.addNote(0, 0, note.pitch, note.start, note.end - note.start, note.velocity)

    with open(f'{path}', "wb") as output_file:
        midi.writeFile(output_file)
