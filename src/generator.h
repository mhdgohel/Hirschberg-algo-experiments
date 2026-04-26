#ifndef GENERATOR_H
#define GENERATOR_H

#include <string>
#include <random>

class Generator {
public:
    // Generate a random DNA sequence of given length
    static std::string generate_random_dna(int length, unsigned int seed = 42) {
        std::mt19937 gen(seed);
        std::uniform_int_distribution<> dis(0, 3);
        const char dna_chars[] = {'A', 'C', 'G', 'T'};
        
        std::string seq;
        seq.reserve(length);
        for (int i = 0; i < length; ++i) {
            seq += dna_chars[dis(gen)];
        }
        return seq;
    }

    // Mutate an existing sequence with a given mutation rate (0.0 to 1.0)
    static std::string mutate_sequence(const std::string& seq, double mutation_rate, unsigned int seed = 42) {
        std::mt19937 gen(seed);
        std::uniform_real_distribution<> dis(0.0, 1.0);
        std::uniform_int_distribution<> char_dis(0, 3);
        const char dna_chars[] = {'A', 'C', 'G', 'T'};
        
        std::string mutated_seq = seq;
        for (size_t i = 0; i < mutated_seq.length(); ++i) {
            if (dis(gen) < mutation_rate) {
                // simple mutation: replace with a random DNA character
                // (could be same character, effectively making actual mutation rate slightly lower)
                mutated_seq[i] = dna_chars[char_dis(gen)];
            }
        }
        return mutated_seq;
    }
};

#endif // GENERATOR_H
