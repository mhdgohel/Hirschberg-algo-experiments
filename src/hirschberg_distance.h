#ifndef HIRSCHBERG_DISTANCE_H
#define HIRSCHBERG_DISTANCE_H

#include <cstdlib>
#include <string>
#include <string_view>
#include <vector>
#include <algorithm>

class HirschbergDistance {
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

    static int hirschberg_recursive(std::string_view A, std::string_view B, bool pivot) {
        int n = A.length();
        int m = B.length();

        if (n == 0) return m;
        if (m == 0) return n;
        if (n == 1 || m == 1) {
            return nw_score(A, B).back();
        }

        int amid = n/2;
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

        int dist1 = hirschberg_recursive(A_first, B_first, pivot);
        int dist2 = hirschberg_recursive(A_second, B_second, pivot);
        
        return dist1 + dist2;
    }

public:
    // Calculates strictly distance using divide and conquer (Space: O(min(N, M)))
    static int distance(const std::string& A, const std::string& B, bool pivot = false) {
        return hirschberg_recursive(A, B, pivot);
    }
};

#endif // HIRSCHBERG_DISTANCE_H
