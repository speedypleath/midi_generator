#include <pybind11/pybind11.h>
#include "include/note.h"

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

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
