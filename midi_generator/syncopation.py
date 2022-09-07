from note import Note
from math import floor


def weighted_note_to_beat(notes: list[Note]) -> float:
    total = 0

    for note in notes:
        left = floor(note.start)
        right = left + 1
        distance = min(note.start - left, abs(note.start - right))

        if distance == 0:
            continue
        if right < note.end < right + 1:
            total += 2 / distance
        else:
            total += 1 / distance

    total /= 5
    return total / len(notes)


def generators(n):
    s = set(range(1, n))
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add((a * x) % n)
        if g == s:
            results.append(a)
    return results


def off_beatness(notes: list[Note], ticks: int) -> float:
    off_beats = generators(ticks)
    weights = [1 if int(x.start * 2) in off_beats else 0 for x in notes]
    return sum(weights) / len(notes)


def density(genes) -> float:
    return len(list(filter(lambda gene: gene.velocity > 0 and gene.velocity > 0, genes))) / len(genes)


def consonance_ratio(genes, config) -> float:
    return len(list(filter(lambda gene: gene.pitch in config.scale.consonant_notes, genes))) / len(genes)
