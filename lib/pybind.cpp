#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "include/note.h"
#include "include/configuration.h"


#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;

PYBIND11_MODULE(note, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: note
        .. autosummary::
           :toctree: _generate
           Note
    )pbdoc";

    pybind11::class_<midi_generator::Note>(m, "Note")
            .def(pybind11::init<int, int, double, double>())
            .def_readwrite("pitch", &midi_generator::Note::pitch)
            .def_readwrite("velocity", &midi_generator::Note::velocity)
            .def_readwrite("start", &midi_generator::Note::start)
            .def_readwrite("end", &midi_generator::Note::end)
            .def("__repr__", [](const midi_generator::Note &note) {
                return "pitch: " + std::to_string(note.pitch) + " velocity: " + std::to_string(note.velocity) + \
                       " start: " + std::to_string(note.start) + " end: " + std::to_string(note.end);
            });

    pybind11::class_<midi_generator::Scale>(m, "Scale")
            .def(pybind11::init<int, int>())
            .def_readwrite("consonant_notes", &midi_generator::Scale::consonant_notes)
            .def_readwrite("dissonant_notes", &midi_generator::Scale::dissonant_notes);

    pybind11::class_<midi_generator::Configuration>(m, "Configuration")
            .def(pybind11::init<>())
            .def_readwrite("syncopation", &midi_generator::Configuration::syncopation)
            .def_readwrite("density", &midi_generator::Configuration::density)
            .def_readwrite("consonance", &midi_generator::Configuration::consonance)
            .def_readwrite("scale", &midi_generator::Configuration::scale)
            .def_readwrite("bars", &midi_generator::Configuration::bars)
            .def_readwrite("rate", &midi_generator::Configuration::rate)
            .def_readwrite("fitness_method", &midi_generator::Configuration::fitness_method)
            .def_readwrite("compression_method", &midi_generator::Configuration::compression_method)
            .def_readwrite("pitch_change_rate", &midi_generator::Configuration::pitch_change_rate)
            .def_readwrite("length_change_rate", &midi_generator::Configuration::length_change_rate)
            .def_readwrite("consonance_rate", &midi_generator::Configuration::consonance_rate)
            .def_readwrite("match", &midi_generator::Configuration::match);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}