#ifndef UTILS_H
#define UTILS_H

#include <chrono>
#include <sys/resource.h>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>

// Timer class for measuring execution time
class Timer {
private:
    std::chrono::high_resolution_clock::time_point start_time;

public:
    void start() {
        start_time = std::chrono::high_resolution_clock::now();
    }

    // Returns elapsed time in milliseconds
    double elapsed_ms() {
        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> duration = end_time - start_time;
        return duration.count();
    }
};

// Returns current peak memory usage in MB
inline double get_peak_memory_mb() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    // On macOS, ru_maxrss is in bytes. On Linux it's in kilobytes.
    // Since user is on macOS, we divide by 1024*1024 to get MB.
#ifdef __APPLE__
    return (double)usage.ru_maxrss / (1024.0 * 1024.0);
#else
    return (double)usage.ru_maxrss / 1024.0;
#endif
}

// Struct to hold experiment results
struct ExperimentResult {
    std::string algorithm;
    int length_A;
    int length_B;
    int edit_distance;
    double time_ms;
    double peak_memory_mb;
};

// Function to save results to CSV
inline void save_results_to_csv(const std::string& filename, const std::vector<ExperimentResult>& results) {
    std::ofstream file(filename);
    if (file.is_open()) {
        file << "algorithm,length_A,length_B,edit_distance,time_ms,peak_memory_mb\n";
        for (const auto& res : results) {
            file << res.algorithm << ","
                 << res.length_A << ","
                 << res.length_B << ","
                 << res.edit_distance << ","
                 << res.time_ms << ","
                 << res.peak_memory_mb << "\n";
        }
        file.close();
        std::cout << "Results saved to " << filename << std::endl;
    } else {
        std::cerr << "Failed to open file: " << filename << std::endl;
    }
}

#endif // UTILS_H
