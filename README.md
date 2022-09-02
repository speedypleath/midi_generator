# Midi generator using genetic algorithms
[![Upload Python Package](https://github.com/speedypleath/midi_generator/actions/workflows/python-publish.yml/badge.svg)](https://github.com/speedypleath/midi_generator/actions/workflows/python-publish.yml)

Requires Python 3.10
## Build
```bash
python3 -m build
pip install dist/*.whl
```

## Api reference
* generate(config: Configuration) - generate a note sequence using given configuration
* mutate(sequence: Sequence, config: Configuration) - mutate sequence 
* continue_sequence(sequence: Sequence, config=Configuration()) - continue sequence
* combine(sequences: list[Sequence], config: Configuration = Configuration()) - combine sequences
* write_file(notes: Sequence, path: str) - write midi file containing sequence at given path