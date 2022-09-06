//
// Created by Andrei Gheorghe on 05.09.2022.
//

#include <ostream>
#include <list>
#include <string>
#include <algorithm>

namespace midi_generator
{
    struct Configuration;
    class Scale;

    enum Key {
        C = 0, D = 1, E = 2, F = 3, G = 4, A = 5, B = 6
    };

    enum Mode {
        Major = 0, Minor = 1, Dorian = 2, Phrygian = 3, Lydian = 4, Mixolydian = 5, Locrian = 6
    };
}

class midi_generator::Scale {
    midi_generator::Key key;
    midi_generator::Mode mode;

    #define VAR_NAME_HELPER(name) #name
    #define VAR_NAME(x) VAR_NAME_HELPER(x)

    #define CHECK_STATE_STR(x) case(x):return VAR_NAME(x);

    static const char *key_to_string(const Key k) {
        switch (k) {
            CHECK_STATE_STR(A)
            CHECK_STATE_STR(B)
            CHECK_STATE_STR(C)
            CHECK_STATE_STR(D)
            CHECK_STATE_STR(E)
            CHECK_STATE_STR(F)
            CHECK_STATE_STR(G)
        }
    }

    static const char *mode_to_string(const Mode m) {
        switch (m) {
            CHECK_STATE_STR(Major)
            CHECK_STATE_STR(Minor)
            CHECK_STATE_STR(Dorian)
            CHECK_STATE_STR(Phrygian)
            CHECK_STATE_STR(Lydian)
            CHECK_STATE_STR(Mixolydian)
            CHECK_STATE_STR(Locrian)
        }
    }

    void generate_notes(int k, const std::list<int>& steps) {
        for(int i = k + 36; i <= k + 48; i += 12)
            for(int j = 0; j < 12; j++)
                if(std::find(steps.begin(), steps.end(), j) != steps.end())
                    consonant_notes.emplace_back(i + j);
                else
                    dissonant_notes.emplace_back(i + j);
    }
public:
    std::list<int> consonant_notes, dissonant_notes;
    Scale(int k, int m): key(static_cast<Key>(k)), mode(static_cast<Mode>(m)) {
        switch (m) {
            case 0:
                generate_notes(key, { 0, 2, 4, 5, 7, 9, 11 });
                break;
            case 1:
                generate_notes(key, { 0, 2, 3, 5, 7, 8, 10 });
                break;
            case 2:
                generate_notes(key, { 0, 1, 3, 5, 7, 8, 10 });
                break;
            case 3:
                generate_notes(key, { 0, 2, 3, 5, 7, 9, 10 });
                break;
            case 4:
                generate_notes(key, { 0, 2, 4, 5, 7, 9, 10 });
                break;
            case 5:
                generate_notes(key, { 0, 2, 4, 5, 7, 9, 11 });
                break;
            case 6:
                generate_notes(key, { 0, 1, 3, 5, 6, 8, 10 });
                break;
            default:
                throw std::exception();
        }
    }
    friend std::ostream &operator<<(std::ostream &os, const Scale &scale) {
        os << "scale " << key_to_string(scale.key) << " " << mode_to_string(scale.mode);
        return os;
    }
};

struct midi_generator::Configuration {
    double syncopation = 0.4f;
    double density = 0.8f;

    double consonance = 0.8f;
    int bars = 4;
    double rate = 1.f / 4;
    std::string fitness_method = "normal";
    std::string compression_method = "LZ77";
    double pitch_change_rate = 0.2f;
    double length_change_rate = 0.1f;
    double consonance_rate = 0.5f;

    std::list<std::string> match{};
    Scale scale = Scale(C, Phrygian);

    friend std::ostream &operator<<(std::ostream &os, const Configuration &configuration) {
        os << "Configuration: syncopation " << configuration.syncopation << ", density " << configuration.density << ", consonance "
           << configuration.consonance << ", bars " << configuration.bars << ", rate " << configuration.rate << ", " << configuration.scale;
        return os;
    }
};