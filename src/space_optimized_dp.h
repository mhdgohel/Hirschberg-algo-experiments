#ifndef SPACE_OPTIMIZED_DP_H
#define SPACE_OPTIMIZED_DP_H

#include <string>
#include <vector>
#include <algorithm>

class SpaceOptimizedDP {
public:
    // Calculates strictly the distance (Space: O(min(N, M)))
    static int distance(const std::string& A, const std::string& B) {
        int n = A.length();
        int m = B.length();

        std::vector<int> prev(m + 1, 0);
        std::vector<int> curr(m + 1, 0);

        for (int j = 0; j <= m; ++j) {
            prev[j] = j;
        }

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

        return prev[m];
    }
};

#endif // SPACE_OPTIMIZED_DP_H
