#include <boost/python.hpp>
#include "note.h"
using namespace boost::python;

template<typename T>
void list_assign(std::list<T>& l, object o) {
    // Turn a Python sequence into an STL input range
    stl_input_iterator<T> begin(o), end;
    l.assign(begin, end);
}

static void* convertible(PyObject* obj) {
    if (!PyTuple_Check(obj)) {
        return 0;
    }
    if (PyTuple_Size(obj) != 4) {
        return 0;
    }
    if (!PyLong_Check(PyTuple_GetItem(obj, 0))) {
        return 0;
    }
    if (!PyLong_Check(PyTuple_GetItem(obj, 1))) {
        return 0;
    }
    if (!PyFloat_Check(PyTuple_GetItem(obj, 2))) {
        return 0;
    }
    if (!PyFloat_Check(PyTuple_GetItem(obj, 3))) {
        return 0;
    }

    return obj;
}

static void construct(PyObject* obj, boost::python::converter::rvalue_from_python_stage1_data* data) {
    void* storage = ((converter::rvalue_from_python_storage<midi_generator::Note>*)data)->storage.bytes;

    new (storage) midi_generator::Note(
        PyLong_AsLong(PyTuple_GetItem(obj, 0)),
        PyLong_AsLong(PyTuple_GetItem(obj, 1)),
        PyFloat_AsDouble(PyTuple_GetItem(obj, 2)),
        PyFloat_AsDouble(PyTuple_GetItem(obj, 3))
    );

    data->convertible = storage;
}

BOOST_PYTHON_MODULE(note)
{
    converter::registry::push_back(&convertible, &construct, type_id<midi_generator::Note>());

    class_<midi_generator::Note>("Note", init<int, int, double, double>())
        .add_property("pitch", &midi_generator::Note::pitch)
        .add_property("velocity", &midi_generator::Note::velocity)
        .add_property("start", &midi_generator::Note::start)
        .add_property("end", &midi_generator::Note::end);
}
