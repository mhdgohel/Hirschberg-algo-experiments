#ifndef HIRSCHBERG_H
#define HIRSCHBERG_H

#include <string>
#include <string_view>
#include <vector>
#include <algorithm>
#include "standard_dp.h"

class HirschbergTrace {
private:
    static std::vector<int> nw_score(std::string_view A, std::string_view B) {
        int n = A.length();
        int m = B.length();
        std::vector<int> prev(m + 1, 0);
        std::vector<int> curr(m + 1, 0);

        for (int j = 0; j <= m; ++j) prev[j] = j;

        for (int i = 1; i <= n; ++i) {
            curr[0] = i;
            for (int j = 1; j <= m; ++j) {
                int cost = (A[i - 1] == B[j - 1]) ? 0 : 1;
                curr[j] = std::min({
                    prev[j] + 1,
                    curr[j - 1] + 1,
                    prev[j - 1] + cost
                });
            }
            prev = curr;
        }
        return prev;
    }

    // Reverse logic without creating string copies
    static std::vector<int> nw_score_rev(std::string_view A, std::string_view B) {
        int n = A.length();
        int m = B.length();
        std::vector<int> prev(m + 1, 0);
        std::vector<int> curr(m + 1, 0);

        for (int j = 0; j <= m; ++j) prev[j] = j;

        for (int i = 1; i <= n; ++i) {
            curr[0] = i;
            for (int j = 1; j <= m; ++j) {
                int cost = (A[n - i] == B[m - j]) ? 0 : 1;
                curr[j] = std::min({
                    prev[j] + 1,
                    curr[j - 1] + 1,
                    prev[j - 1] + cost
                });
            }
            prev = curr;
        }
        return prev;
    }

    static void hirschberg_recursive(std::string_view A, std::string_view B, std::string& aligned_A, std::string& aligned_B, bool pivot) {
        int n = A.length();
        int m = B.length();

        if (n == 0) {
            for (int i = 0; i < m; ++i) {
                aligned_A += '-';
                aligned_B += B[i];
            }
        } else if (m == 0) {
            for (int i = 0; i < n; ++i) {
                aligned_A += A[i];
                aligned_B += '-';
            }
        } else if (n == 1 || m == 1) {
            auto res = StandardDP::align(std::string(A), std::string(B));
            aligned_A += res.aligned_A;
            aligned_B += res.aligned_B;
        } else {
            int amid = n / 2;
            if(pivot){
                amid = rand()%n;
            }
            std::string_view A_first = A.substr(0, amid);
            std::string_view A_second = A.substr(amid);

            std::vector<int> score_L = nw_score(A_first, B);
            std::vector<int> score_R_rev = nw_score_rev(A_second, B);

            int bmid = 0;
            int min_score = 1e9;
            for (int j = 0; j <= m; ++j) {
                if (score_L[j] + score_R_rev[m - j] < min_score) {
                    min_score = score_L[j] + score_R_rev[m - j];
                    bmid = j;
                }
            }

            std::string_view B_first = B.substr(0, bmid);
            std::string_view B_second = B.substr(bmid);

            hirschberg_recursive(A_first, B_first, aligned_A, aligned_B, pivot);
            hirschberg_recursive(A_second, B_second, aligned_A, aligned_B, pivot);
        }
    }

public:
    // Calculates Trace (Space: O(N+M) for trace string + O(M) for DP)
    static StandardDP::Result align(const std::string& A, const std::string& B, bool pivot = false) {
        std::string aligned_A = "";
        std::string aligned_B = "";
        
        aligned_A.reserve(A.length() + B.length());
        aligned_B.reserve(A.length() + B.length());

        hirschberg_recursive(A, B, aligned_A, aligned_B, pivot);
        
        int distance = 0;
        for (size_t i = 0; i < aligned_A.length(); ++i) {
            if (aligned_A[i] == '-' || aligned_B[i] == '-' || aligned_A[i] != aligned_B[i]) {
                distance++;
            }
        }

        return {distance, aligned_A, aligned_B};
    }
};

#endif // HIRSCHBERG_H
