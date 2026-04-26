#ifndef STANDARD_DP_H
#define STANDARD_DP_H

#include <string>
#include <vector>
#include <algorithm>

class StandardDP {
public:
    struct Result {
        int distance;
        std::string aligned_A;
        std::string aligned_B;
    };

    static Result align(const std::string& A, const std::string& B) {
        int n = A.length();
        int m = B.length();

        // DP table: (n+1) x (m+1)
        // Memory complexity: O(nm)
        std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));

        // Initialization
        for (int i = 0; i <= n; ++i) dp[i][0] = i;
        for (int j = 0; j <= m; ++j) dp[0][j] = j;

        // DP filling
        for (int i = 1; i <= n; ++i) {
            for (int j = 1; j <= m; ++j) {
                int cost = (A[i - 1] == B[j - 1]) ? 0 : 1;
                dp[i][j] = std::min({
                    dp[i - 1][j] + 1,       // deletion
                    dp[i][j - 1] + 1,       // insertion
                    dp[i - 1][j - 1] + cost // match/mismatch
                });
            }
        }

        // Backtracking
        std::string aligned_A = "";
        std::string aligned_B = "";
        int i = n, j = m;
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0) {
                int cost = (A[i - 1] == B[j - 1]) ? 0 : 1;
                if (dp[i][j] == dp[i - 1][j - 1] + cost) {
                    aligned_A += A[i - 1];
                    aligned_B += B[j - 1];
                    i--; j--;
                    continue;
                }
            }
            if (i > 0 && dp[i][j] == dp[i - 1][j] + 1) {
                aligned_A += A[i - 1];
                aligned_B += '-';
                i--;
            } else {
                aligned_A += '-';
                aligned_B += B[j - 1];
                j--;
            }
        }

        std::reverse(aligned_A.begin(), aligned_A.end());
        std::reverse(aligned_B.begin(), aligned_B.end());

        return {dp[n][m], aligned_A, aligned_B};
    }
};

#endif // STANDARD_DP_H
