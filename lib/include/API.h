#pragma once
#include "note.h"
#include <list>

namespace midi_generator
{
    std::list<Note> generate();
    std::list<Note> mutate(std::list<Note>);
    std::list<Note> continue_sequence(std::list<Note>);
    std::list<Note> combine(const std::list<std::list<Note>>& sequences);
    void save_file(std::list<Note> notes, const std::string& filename);
}