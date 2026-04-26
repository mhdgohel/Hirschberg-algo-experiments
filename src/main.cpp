#include <iostream>
#include <string>
#include "generator.h"
#include "utils.h"
#include "standard_dp.h"
#include "space_optimized_dp.h"
#include "hirschberg.h"
#include "hirschberg_distance.h"

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <algorithm> <length_A> <length_B>\n";
        return 1;
    }

    std::string algo = argv[1];
    int N = std::stoi(argv[2]);
    int M = std::stoi(argv[3]);
    bool pivot = false;
    if (argc == 5) {
        pivot = std::stoi(argv[4]) == 1;
    }

    std::string A = Generator::generate_random_dna(N, 42);
    std::string B = (N == M) ? Generator::mutate_sequence(A, 0.1, 42) : Generator::generate_random_dna(M, 43);

    Timer timer;
    int distance = 0;

    timer.start();
    if (algo == "standard_trace") {
        auto res = StandardDP::align(A, B);
        distance = res.distance;
    } else if (algo == "hirschberg_trace") {
        auto res = HirschbergTrace::align(A, B, pivot);
        distance = res.distance;
    } else if (algo == "optimized_distance") {
        distance = SpaceOptimizedDP::distance(A, B);
    } else if (algo == "hirschberg_distance") {
        distance = HirschbergDistance::distance(A, B, pivot);
    } else {
        std::cerr << "Unknown algorithm: " << algo << "\n";
        return 1;
    }

    double time_ms = timer.elapsed_ms();
    double mem_mb = get_peak_memory_mb();

    if(algo == "hirschberg_trace" || algo == "hirschberg_distance")
    {
        if(pivot) algo = "hirschberg_pivot";
    }

    std::cout << algo << "," << N << "," << M << "," << distance << "," << time_ms << "," << mem_mb << "\n";

    return 0;
}
