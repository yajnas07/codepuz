#include <ranges>
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <numeric>

// Helper function to print a range
template<std::ranges::range R>
void print(const std::string& label, R&& r) {
    std::cout << label << ": ";
    for (const auto& elem : r) {
        std::cout << elem << " ";
    }
    std::cout << "\n";
}

int main() {
    std::cout << "=== C++20 Range Algorithms Demo ===\n\n";

    // Sample data
    std::vector<int> numbers = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};
    print("Original numbers", numbers);

    // -----------------------------------------------
    // 1. std::ranges::sort - Sort elements
    // -----------------------------------------------
    std::cout << "\n--- 1. ranges::sort ---\n";
    std::vector<int> sorted_nums = numbers;
    std::ranges::sort(sorted_nums);
    print("Sorted (ascending)", sorted_nums);

    //Same as 
    // std::ranges::sort(sorted_nums, [](int a, int b) { return a > b; });
    std::ranges::sort(sorted_nums, std::greater{});
    print("Sorted (descending)", sorted_nums);
    
    // -----------------------------------------------
    // 2. std::ranges::find / find_if - Find elements
    // -----------------------------------------------
    std::cout << "\n--- 2. ranges::find / find_if ---\n";
    auto it = std::ranges::find(numbers, 7);
    if (it != numbers.end()) {
        std::cout << "Found 7 at position: " << std::distance(numbers.begin(), it) << "\n";
    }
    
    auto it2 = std::ranges::find_if(numbers, [](int x) { return x > 8; });
    if (it2 != numbers.end()) {
        std::cout << "First element > 8: " << *it2 << " At position: " << std::distance(numbers.begin(), it2) << "\n";
    }
    
    // -----------------------------------------------
    // 3. std::ranges::count / count_if - Count elements
    // -----------------------------------------------
    std::cout << "\n--- 3. ranges::count / count_if ---\n";
    auto even_count = std::ranges::count_if(numbers, [](int x) { return x % 2 == 0; });
    std::cout << "Count of even numbers: " << even_count << "\n";
    
    std::cout << "Counting prime numbers using count_if: Found:";
    auto prime_count = std::ranges::count_if(numbers, [](int x) { 
        auto is_prime = [](int n) {
            if (n <= 1) return false;
            for (int i = 2; i * i <= n; ++i) {
                if (n % i == 0) return false;
            }
            return true;
        };
        if (is_prime(x)) {
            std::cout << x << " ";
            return true;
        }
        return false; 
    });
    std::cout << "\nCount of prime numbers: " << prime_count << "\n";
    
    // -----------------------------------------------
    // 4. std::ranges::transform - Transform elements
    // -----------------------------------------------
    std::cout << "\n--- 4. ranges::transform ---\n";
    std::vector<int> squared(numbers.size());
    std::ranges::transform(numbers, squared.begin(), [](int x) { return x * x; });
    print("Squared values", squared);
    
    // -----------------------------------------------
    // 5. std::ranges::copy_if - Copy with condition
    // -----------------------------------------------
    std::cout << "\n--- 5. ranges::copy_if ---\n";
    std::vector<int> evens;
    std::ranges::copy_if(numbers, std::back_inserter(evens), [](int x) { return x % 2 == 0; });
    print("Even numbers only", evens);
    
    // -----------------------------------------------
    // 6. std::ranges::all_of / any_of / none_of
    // -----------------------------------------------
    std::cout << "\n--- 6. ranges::all_of / any_of / none_of ---\n";
    bool all_positive = std::ranges::all_of(numbers, [](int x) { return x > 0; });
    std::cout << "All positive? " << std::boolalpha << all_positive << "\n";
    
    bool any_greater_than_5 = std::ranges::any_of(numbers, [](int x) { return x > 5; });
    std::cout << "Any > 5? " << any_greater_than_5 << "\n";
    
    bool none_negative = std::ranges::none_of(numbers, [](int x) { return x < 0; });
    std::cout << "None negative? " << none_negative << "\n";
    
    // -----------------------------------------------
    // 7. std::ranges::min / max / minmax
    // -----------------------------------------------
    std::cout << "\n--- 7. ranges::min / max / minmax ---\n";
    auto min_val = std::ranges::min(numbers);
    auto max_val = std::ranges::max(numbers);
    auto [min_elem, max_elem] = std::ranges::minmax(numbers);
    std::cout << "Min: " << min_val << ", Max: " << max_val << "\n";
    std::cout << "Minmax: [" << min_elem << ", " << max_elem << "]\n";
    
    // -----------------------------------------------
    // 8. std::ranges::reverse - Reverse elements
    // -----------------------------------------------
    std::cout << "\n--- 8. ranges::reverse ---\n";
    std::vector<int> to_reverse = numbers;
    std::ranges::reverse(to_reverse);
    print("Reversed", to_reverse);
    
    // -----------------------------------------------
    // 9. std::ranges::unique - Remove consecutive duplicates
    // -----------------------------------------------
    std::cout << "\n--- 9. ranges::unique ---\n";
    std::vector<int> with_dups = {1, 1, 2, 2, 2, 3, 3, 4, 5, 5};
    print("With duplicates", with_dups);
    auto [first, last] = std::ranges::unique(with_dups);
    with_dups.erase(first, last);
    print("After unique", with_dups);
    
    // -----------------------------------------------
    // 10. std::ranges::remove_if - Remove elements
    // -----------------------------------------------
    std::cout << "\n--- 10. ranges::remove_if ---\n";
    std::vector<int> to_remove = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    print("Before remove_if (odds)", to_remove);
    auto [rem_first, rem_last] = std::ranges::remove_if(to_remove, [](int x) { return x % 2 != 0; });
    to_remove.erase(rem_first, rem_last);
    print("After remove_if", to_remove);
    
    // -----------------------------------------------
    // 11. std::ranges::fill - Fill with value
    // -----------------------------------------------
    std::cout << "\n--- 11. ranges::fill ---\n";
    std::vector<int> filled(5);
    std::ranges::fill(filled, 42);
    print("Filled with 42", filled);
    
    // -----------------------------------------------
    // 12. std::ranges::generate - Generate values
    // -----------------------------------------------
    std::cout << "\n--- 12. ranges::generate ---\n";
    std::vector<int> generated(10);
    int counter = 0;
    std::ranges::generate(generated, [&counter]() { return counter++; });
    print("Generated sequence", generated);
    
    // -----------------------------------------------
    // 13. std::ranges::replace_if - Replace conditionally
    // -----------------------------------------------
    std::cout << "\n--- 13. ranges::replace_if ---\n";
    std::vector<int> to_replace = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    print("Before replace_if", to_replace);
    std::ranges::replace_if(to_replace, [](int x) { return x % 2 == 0; }, 0);
    print("After replacing evens with 0", to_replace);

    // -----------------------------------------------
    // 14. std::ranges::partition - Partition elements
    // -----------------------------------------------
    std::cout << "\n--- 14. ranges::partition ---\n";
    std::vector<int> to_partition = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};
    print("Before partition", to_partition);
    auto pivot = std::ranges::partition(to_partition, [](int x) { return x <= 5; });
    print("After partition (<=5 | >5)", to_partition);
    std::cout << "Partition point at index: " << std::distance(to_partition.begin(), pivot.begin()) << "\n";
    
    // -----------------------------------------------
    // 15. std::ranges::is_sorted - Check if sorted
    // -----------------------------------------------
    std::cout << "\n--- 15. ranges::is_sorted ---\n";
    std::vector<int> sorted_check = {1, 2, 3, 4, 5};
    std::vector<int> unsorted_check = {3, 1, 4, 1, 5};
    std::cout << "{1,2,3,4,5} is sorted? " << std::ranges::is_sorted(sorted_check) << "\n";
    std::cout << "{3,1,4,1,5} is sorted? " << std::ranges::is_sorted(unsorted_check) << "\n";

    // -----------------------------------------------
    // 16. std::ranges::binary_search - Binary search
    // -----------------------------------------------
    std::cout << "\n--- 16. ranges::binary_search ---\n";
    std::vector<int> sorted_for_search = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    bool found_5 = std::ranges::binary_search(sorted_for_search, 5);
    bool found_11 = std::ranges::binary_search(sorted_for_search, 11);
    std::cout << "Binary search for 5: " << found_5 << "\n";
    std::cout << "Binary search for 11: " << found_11 << "\n";

    // -----------------------------------------------
    // 17. std::ranges::nth_element - Partial sort
    // -----------------------------------------------
    std::cout << "\n--- 17. ranges::nth_element ---\n";
    std::vector<int> for_nth = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};
    print("Before nth_element", for_nth);
    std::ranges::nth_element(for_nth, for_nth.begin() + 4); // 5th smallest
    std::cout << "5th smallest element (median-ish): " << for_nth[4] << "\n";
    print("After nth_element", for_nth);

    // -----------------------------------------------
    // 18. Working with strings
    // -----------------------------------------------
    std::cout << "\n--- 18. Ranges with strings ---\n";
    std::vector<std::string> names = {"Alice", "Bob", "Charlie", "David", "Eve"};
    print("Original names", names);

    std::ranges::sort(names, [](const auto& a, const auto& b) {
        return a.length() < b.length();
    });
    print("Sorted by length", names);

    // -----------------------------------------------
    // 19. Projection - Access members elegantly
    // -----------------------------------------------
    std::cout << "\n--- 19. Projections ---\n";
    struct Person {
        std::string name;
        int age;
    };

    std::vector<Person> people = {
        {"Alice", 30}, {"Bob", 25}, {"Charlie", 35}, {"David", 28}
    };

    // Sort by age using projection
    std::ranges::sort(people, {}, &Person::age);
    std::cout << "People sorted by age:\n";
    for (const auto& p : people) {
        std::cout << "  " << p.name << ": " << p.age << "\n";
    }

    // Find person by name using projection
    auto person_it = std::ranges::find(people, "Charlie", &Person::name);
    if (person_it != people.end()) {
        std::cout << "Found Charlie, age: " << person_it->age << "\n";
    }

    // -----------------------------------------------
    // 20. Combining with views (range adaptors)
    // -----------------------------------------------
    std::cout << "\n--- 20. Combining algorithms with views ---\n";
    std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Filter evens, transform to squares, take first 3
    auto result = data
        | std::views::filter([](int x) { return x % 2 == 0; })
        | std::views::transform([](int x) { return x * x; })
        | std::views::take(3);

    std::cout << "Evens -> squared -> first 3: ";
    for (int x : result) {
        std::cout << x << " ";
    }
    std::cout << "\n";

    std::cout << "\n=== Demo Complete ===\n";
    return 0;
}
