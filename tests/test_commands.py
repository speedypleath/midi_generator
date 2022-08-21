from midi_generator.cli.commands import generate
from midi_generator.config import Configuration


def test_generate():
    notes = generate(Configuration())
    print(notes)
    assert(notes != None)