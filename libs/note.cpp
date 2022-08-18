#include <boost/python.hpp>
using namespace boost::python;

struct Note {
    Note(uint8_t pitch, uint8_t velocity, double start, double end) : pitch(pitch), velocity(velocity), start(start), end(end) {}
    uint8_t pitch;
    uint8_t velocity;
    double start;
    double end; 
};

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
    void* storage = ((converter::rvalue_from_python_storage<Note>*)data)->storage.bytes;

    new (storage) Note(
        PyLong_AsLong(PyTuple_GetItem(obj, 0)),
        PyLong_AsLong(PyTuple_GetItem(obj, 1)),
        PyFloat_AsDouble(PyTuple_GetItem(obj, 2)),
        PyFloat_AsDouble(PyTuple_GetItem(obj, 3))
    );

    data->convertible = storage;
}

BOOST_PYTHON_MODULE(note)
{
    converter::registry::push_back(&convertible, &construct, type_id<Note>());

    class_<Note>("Note", init<int, int, double, double>())
        .add_property("pitch", &Note::pitch)
        .add_property("velocity", &Note::velocity)
        .add_property("start", &Note::start)
        .add_property("end", &Note::end);
}
