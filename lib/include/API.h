#pragma once
#include "note.h"
#include "configuration.h"
#include <list>

namespace midi_generator
{
    std::list<Note> generate();
    std::list<Note> mutate(const std::list<midi_generator::Note>&);
    std::list<Note> continue_sequence(const std::list<midi_generator::Note>&);
    std::list<Note> combine(const std::list<std::list<Note>>& sequences);
    std::list<Note> generate(const midi_generator::Configuration&);
    std::list<Note> mutate(std::list<midi_generator::Note>, const midi_generator::Configuration&);
    std::list<Note> continue_sequence(std::list<midi_generator::Note>, const midi_generator::Configuration&);
    std::list<Note> combine(const std::list<std::list<Note>>&, const midi_generator::Configuration&);
    void save_file(std::list<Note> notes, const std::string& filename);
}