from midiutil import MIDIFile
from note import Note


def write_file(notes: list[Note], file_name: str):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)

    for note in notes:
        midi.addNote(0, 0, note.pitch, note.start, note.end - note.start, note.velocity)

    with open(f'midi/{file_name}.mid', "wb") as output_file:
        midi.writeFile(output_file)
