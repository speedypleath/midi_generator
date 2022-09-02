#pragma once
#include "note.h"
#include <list>
#include <pybind11/pybind11.h>

namespace midi_generator
{
    std::list<Note> generate();
    std::list<Note> mutate(std::list<Note>);
    std::list<Note> continue_sequence();
    std::list<Note> combine();
    void save_file(std::string filename, std::list<Note> notes);
}