# C++20 Range Algorithms - Line by Line Explanation

## 1. `std::ranges::sort` - Sorting Elements

```cpp
std::vector<int> sorted_nums = numbers;
```
Creates a **copy** of the original `numbers` vector because `ranges::sort` modifies the container **in-place**.

---

```cpp
std::ranges::sort(sorted_nums);
```
Sorts `sorted_nums` in **ascending order** (smallest to largest).

**Key differences from classic `std::sort`:**

| Classic `std::sort` | `std::ranges::sort` |
|---------------------|---------------------|
| `std::sort(vec.begin(), vec.end())` | `std::ranges::sort(vec)` |
| Requires iterator pair | Accepts the **entire range** directly |
| Error-prone (mismatched iterators) | Safer, cleaner syntax |

**Result:** `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}` → `{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}`

---

```cpp
std::ranges::sort(sorted_nums, std::greater{});
```
Sorts `sorted_nums` in **descending order** (largest to smallest).

- `std::greater{}` is a **comparator** (function object) that returns `true` if the first argument is greater than the second
- Equivalent to: `std::ranges::sort(sorted_nums, [](int a, int b) { return a > b; })`
- `std::greater{}` uses **CTAD** (Class Template Argument Deduction) - the `<int>` is automatically deduced

**Result:** `{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}` → `{10, 9, 8, 7, 6, 5, 4, 3, 2, 1}`

---

### Function Signature

```cpp
template<std::random_access_range R, class Comp = std::ranges::less, class Proj = std::identity>
constexpr ranges::borrowed_iterator_t<R>
    sort(R&& r, Comp comp = {}, Proj proj = {});
```

**Parameters:**
- `r` - The range to sort
- `comp` - Comparator (defaults to `std::ranges::less` for ascending)
- `proj` - Projection (we'll cover this in example 19)

---

## 2. `std::ranges::find` / `find_if` - Finding Elements

```cpp
auto it = std::ranges::find(numbers, 7);
```
Searches for the value `7` in `numbers`. Returns an **iterator** to the first matching element, or `numbers.end()` if not found.

- Unlike `std::find(begin, end, val)`, you pass the **entire range**
- The return type is deduced as `std::vector<int>::iterator`

---

```cpp
if (it != numbers.end()) {
    std::cout << "Found 7 at position: " << std::distance(numbers.begin(), it) << "\n";
}
```
- Always check if the iterator is valid before dereferencing
- `std::distance(numbers.begin(), it)` calculates the **index** (0-based position)

---

```cpp
auto it2 = std::ranges::find_if(numbers, [](int x) { return x > 8; });
```
Searches for the **first element** that satisfies a **predicate** (condition).

- The lambda `[](int x) { return x > 8; }` returns `true` for elements greater than 8
- In `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}`, the first element > 8 is `9`

**When to use which:**
| `find` | `find_if` |
|--------|-----------|
| Search by **exact value** | Search by **condition/predicate** |
| `find(range, 7)` | `find_if(range, [](int x) { return x > 8; })` |

---

## 3. `std::ranges::count` / `count_if` - Counting Elements

```cpp
auto even_count = std::ranges::count_if(numbers, [](int x) { return x % 2 == 0; });
```
Counts how many elements satisfy the predicate. Returns a **count** (integer), not an iterator.

- `x % 2 == 0` checks if a number is even
- In `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}`, there are **5 even numbers**: 2, 8, 4, 6, 10

---

```cpp
auto prime_count = std::ranges::count_if(numbers, [](int x) { 
    auto is_prime = [](int n) { /* ... */ };
    if (is_prime(x)) {
        std::cout << x << " ";
        return true;
    }
    return false; 
});
```
Counts **prime numbers** in the range. The nested `is_prime` lambda checks if a number is prime.

- In `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}`, the primes are: **2, 3, 5, 7** (count = 4)
- Note: The lambda also prints each prime as a side effect

**`count` vs `count_if`:**
| `count` | `count_if` |
|---------|------------|
| Count by **exact value** | Count by **condition** |
| `count(range, 5)` - how many 5s? | `count_if(range, pred)` - how many match? |

**Return type:** `std::ranges::range_difference_t<R>` (typically `ptrdiff_t` or `long`)

---
## 4. `std::ranges::transform` - Transforming Elements

```cpp
std::vector<int> squared(numbers.size());
```
Allocates a **pre-sized output vector** to hold the results. `transform` writes to an existing destination - it does not append or resize.

---

```cpp
std::ranges::transform(numbers, squared.begin(), [](int x) { return x * x; });
```
Applies the lambda to **each element** of `numbers` and writes the result into `squared`.

- `numbers` is the **input range**
- `squared.begin()` is the **output iterator** (where results are written)
- `[](int x) { return x * x; }` is the **transform function** - squares each element
- In `{5, 2, 8, 1, 9, ...}` → `{25, 4, 64, 1, 81, ...}`

**Important:** The output range must have at least as many elements as the input, or you get undefined behaviour. That's why we pre-size with `numbers.size()`.

**Comparison with classic `std::transform`:**
| Classic | Ranges |
|---------|--------|
| `std::transform(in.begin(), in.end(), out.begin(), fn)` | `std::ranges::transform(in, out.begin(), fn)` |

---

## 5. `std::ranges::copy_if` - Conditional Copying

```cpp
std::vector<int> evens;
std::ranges::copy_if(numbers, std::back_inserter(evens), [](int x) { return x % 2 == 0; });
```
Copies elements that satisfy the predicate into a destination.

- **`std::back_inserter(evens)`** — creates an output iterator that calls `push_back()` on each write, allowing the vector to grow dynamically
- Unlike `transform`, you don't need to pre-size the output
- In `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}` → copies `{2, 8, 4, 6, 10}` (even numbers only)

**Related algorithms:**
| Algorithm | Description |
|-----------|-------------|
| `copy` | Copy all elements |
| `copy_if` | Copy elements matching a predicate |
| `copy_n` | Copy first n elements |

---

## 6. `std::ranges::all_of` / `any_of` / `none_of` - Boolean Predicates

These three algorithms test whether elements satisfy a condition and return a **boolean**.

```cpp
bool all_positive = std::ranges::all_of(numbers, [](int x) { return x > 0; });
```
Returns `true` if **every element** satisfies the predicate. Here: "Are all numbers positive?" → `true`

---

```cpp
bool any_greater_than_5 = std::ranges::any_of(numbers, [](int x) { return x > 5; });
```
Returns `true` if **at least one element** satisfies the predicate. Here: "Is any number > 5?" → `true` (6, 7, 8, 9, 10)

---

```cpp
bool none_negative = std::ranges::none_of(numbers, [](int x) { return x < 0; });
```
Returns `true` if **no element** satisfies the predicate. Here: "Are there no negative numbers?" → `true`

**Summary:**
| Algorithm | Returns `true` when |
|-----------|---------------------|
| `all_of` | **All** elements match |
| `any_of` | **At least one** matches |
| `none_of` | **Zero** elements match |

**Note:** All three short-circuit — they stop iterating as soon as the result is determined.

---

## 7. `std::ranges::min` / `max` / `minmax` - Finding Extremes

```cpp
auto min_val = std::ranges::min(numbers);
auto max_val = std::ranges::max(numbers);
```
Returns the **minimum** or **maximum** element in the range. Returns the actual **value**, not an iterator.

- In `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}`: `min` → `1`, `max` → `10`

---

```cpp
auto [min_elem, max_elem] = std::ranges::minmax(numbers);
```
Returns **both** min and max in a single pass as a `std::ranges::minmax_result` (a pair-like struct).

- Uses **structured bindings** (`auto [min_elem, max_elem]`) to unpack the result
- More efficient than calling `min` and `max` separately (single traversal vs two)

**Note:** These throw `std::ranges::bad_range_access` if the range is empty. For iterators to the elements instead of values, use `min_element`, `max_element`, `minmax_element`.

---

## 8. `std::ranges::reverse` - Reversing Elements

```cpp
std::vector<int> to_reverse = numbers;
std::ranges::reverse(to_reverse);
```
Reverses elements **in-place**. No return value (mutates the container directly).

- `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}` → `{10, 6, 4, 7, 3, 9, 1, 8, 2, 5}`

**For a non-mutating version**, use `std::views::reverse`:
```cpp
for (int x : numbers | std::views::reverse) { /* ... */ }
```
This creates a **lazy view** without modifying the original container.

---

## 9. `std::ranges::unique` - Remove Consecutive Duplicates

```cpp
std::vector<int> with_dups = {1, 1, 2, 2, 2, 3, 3, 4, 5, 5};
auto [first, last] = std::ranges::unique(with_dups);
with_dups.erase(first, last);
```
Removes **consecutive duplicate** elements by shifting unique elements to the front.

- Returns a **subrange** `[first, last)` representing the "garbage" at the end (elements to be erased)
- Does **not** resize the container — you must call `.erase()` to actually remove them
- **Important:** Only removes **adjacent** duplicates. For non-adjacent duplicates, sort first!

**Before:** `{1, 1, 2, 2, 2, 3, 3, 4, 5, 5}` → **After `unique`:** `{1, 2, 3, 4, 5, ?, ?, ?, ?, ?}` → **After `erase`:** `{1, 2, 3, 4, 5}`

**Erase-remove idiom** (ranges style):
```cpp
auto [first, last] = std::ranges::unique(vec);
vec.erase(first, last);
```

---

## 10. `std::ranges::remove_if` - Conditional Removal

```cpp
std::vector<int> to_remove = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
auto [rem_first, rem_last] = std::ranges::remove_if(to_remove, [](int x) { return x % 2 != 0; });
to_remove.erase(rem_first, rem_last);
```
Moves elements **not matching** the predicate to the front, returns a subrange of "garbage" to erase.

- Predicate `x % 2 != 0` matches odd numbers → removes odds, keeps evens
- Like `unique`, returns a subrange; you must call `.erase()` to shrink the container

**Before:** `{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}` → **After:** `{2, 4, 6, 8, 10}`

**`remove` vs `remove_if`:**
| Algorithm | Usage |
|-----------|-------|
| `remove(range, value)` | Remove all elements equal to `value` |
| `remove_if(range, pred)` | Remove elements matching a predicate |

**Why the two-step pattern?** Range algorithms don't know how to resize containers (they work with iterators). The container's `.erase()` method handles the actual removal.

---

## 11. `std::ranges::fill` - Fill with a Value

```cpp
std::vector<int> filled(5);
std::ranges::fill(filled, 42);
```
Assigns the same value to **every element** in the range.

- Pre-size the vector (here, 5 elements initialized to 0)
- `fill` overwrites each element with `42`
- **Result:** `{42, 42, 42, 42, 42}`

**Related algorithms:**
| Algorithm | Description |
|-----------|-------------|
| `fill` | Fill entire range with a value |
| `fill_n` | Fill first n elements with a value |

---

## 12. `std::ranges::generate` - Generate Values with a Function

```cpp
std::vector<int> generated(10);
int counter = 0;
std::ranges::generate(generated, [&counter]() { return counter++; });
```
Assigns values by **calling a generator function** for each element.

- The lambda `[&counter]() { return counter++; }` captures `counter` by reference
- Each call returns the current value and increments: 0, 1, 2, 3, ...
- **Result:** `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}`

**`fill` vs `generate`:**
| `fill` | `generate` |
|--------|------------|
| Same value for all elements | Different value per element |
| `fill(range, 42)` | `generate(range, fn)` |

**Common use cases for `generate`:**
- Sequential numbers (like above)
- Random numbers: `generate(vec, []() { return rand(); })`
- Computed values based on state

---

## 13. `std::ranges::replace_if` - Conditional Replacement

```cpp
std::vector<int> to_replace = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
print("Before replace_if", to_replace);
std::ranges::replace_if(to_replace, [](int x) { return x % 2 == 0; }, 0);
print("After replacing evens with 0", to_replace);
```

---

```cpp
std::vector<int> to_replace = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
```
Creates a vector with values 1 through 10.

---

```cpp
std::ranges::replace_if(to_replace, [](int x) { return x % 2 == 0; }, 0);
```
Replaces **in-place** every element that satisfies the predicate with the given new value.

- `to_replace` — the range to modify
- `[](int x) { return x % 2 == 0; }` — the predicate: matches **even numbers**
- `0` — the **replacement value**

The algorithm scans each element. If the predicate returns `true`, the element is overwritten with the replacement value. Elements that don't match are left untouched.

**Before:** `{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}`
**After:** `{1, 0, 3, 0, 5, 0, 7, 0, 9, 0}`

**`replace` vs `replace_if`:**
| Algorithm | Usage |
|-----------|-------|
| `replace(range, old_val, new_val)` | Replace all elements equal to `old_val` |
| `replace_if(range, pred, new_val)` | Replace elements matching a predicate |

**Key difference from `remove_if`:**
- `remove_if` **eliminates** matching elements (shifts non-matching forward)
- `replace_if` **overwrites** matching elements with a new value (container size stays the same)

**Return type:** `ranges::borrowed_iterator_t<R>` — an iterator past the last element examined (i.e., the end of the range).

---

## 14. `std::ranges::partition` - Partitioning Elements

```cpp
std::vector<int> to_partition = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};
print("Before partition", to_partition);
auto pivot = std::ranges::partition(to_partition, [](int x) { return x <= 5; });
print("After partition (<=5 | >5)", to_partition);
std::cout << "Partition point at index: "
          << std::distance(to_partition.begin(), pivot.begin()) << "\n";
```

---

```cpp
std::vector<int> to_partition = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};
```
Creates a vector of unsorted integers.

---

```cpp
auto pivot = std::ranges::partition(to_partition, [](int x) { return x <= 5; });
```
Rearranges elements **in-place** so that all elements satisfying the predicate come **before** those that don't.

- `[](int x) { return x <= 5; }` — the predicate: elements ≤ 5 go to the **left** partition
- Returns a **subrange** representing the second partition (elements that don't satisfy the predicate)
- The **relative order** within each partition is **not preserved** (unstable partition)

**Before:** `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}`
**After (one possible result):** `{5, 2, 4, 1, 3, | 9, 7, 8, 6, 10}` (exact order within partitions may vary)

---

```cpp
std::cout << "Partition point at index: "
          << std::distance(to_partition.begin(), pivot.begin()) << "\n";
```
The returned subrange `pivot` starts at the **partition point** — the first element of the second group. `std::distance` gives its 0-based index.

- In this case, 5 elements satisfy `x <= 5`, so the partition point is at index **5**

**Related algorithms:**
| Algorithm | Description |
|-----------|-------------|
| `partition(range, pred)` | Unstable partition — order within groups not guaranteed |
| `stable_partition(range, pred)` | Stable partition — preserves relative order within each group |
| `is_partitioned(range, pred)` | Checks if a range is already partitioned |
| `partition_point(range, pred)` | Finds the partition point in an already-partitioned range |

**How partition works internally:**
The algorithm uses a two-pointer approach — one scanning from the left for elements that **don't** satisfy the predicate, and one from the right for elements that **do**. When both find misplaced elements, they swap. This gives **O(n)** time complexity with **O(1)** extra space.

**Use cases:**
- Quick-select / quicksort pivot step
- Separating data into two groups (e.g., pass/fail, positive/negative)
- Filtering in-place without allocating a second container

---

## 15. `std::ranges::is_sorted` - Check if Sorted

```cpp
std::vector<int> sorted_check = {1, 2, 3, 4, 5};
std::vector<int> unsorted_check = {3, 1, 4, 1, 5};
std::cout << "{1,2,3,4,5} is sorted? " << std::ranges::is_sorted(sorted_check) << "\n";
std::cout << "{3,1,4,1,5} is sorted? " << std::ranges::is_sorted(unsorted_check) << "\n";
```

---

```cpp
std::ranges::is_sorted(sorted_check)
```
Returns `true` if the range is sorted in **non-descending order** (each element ≤ the next). This is a **non-mutating** check — it does not modify the range.

- `{1, 2, 3, 4, 5}` → `true` (each element ≤ next)
- `{3, 1, 4, 1, 5}` → `false` (3 > 1 violates the ordering)

**Default comparison** is `std::ranges::less` (ascending). You can provide a custom comparator:
```cpp
// Check if sorted in descending order
std::ranges::is_sorted(vec, std::greater{});
```

**Short-circuits:** Stops scanning as soon as it finds a pair of elements out of order — **O(n)** worst case, but can be faster.

**Related algorithms:**
| Algorithm | Description |
|-----------|-------------|
| `is_sorted(range)` | Returns `true`/`false` |
| `is_sorted_until(range)` | Returns iterator to the **first out-of-order** element |

```cpp
auto it = std::ranges::is_sorted_until(unsorted_check);
// it points to element 1 (index 1), since 3 > 1
```

**Use cases:**
- Pre-condition checks before calling algorithms that require sorted input (`binary_search`, `lower_bound`, `merge`)
- Assertions / debugging

---

## 16. `std::ranges::binary_search` - Binary Search

```cpp
std::vector<int> sorted_for_search = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
bool found_5 = std::ranges::binary_search(sorted_for_search, 5);
bool found_11 = std::ranges::binary_search(sorted_for_search, 11);
std::cout << "Binary search for 5: " << found_5 << "\n";
std::cout << "Binary search for 11: " << found_11 << "\n";
```

---

```cpp
std::ranges::binary_search(sorted_for_search, 5)
```
Performs a **binary search** on a sorted range. Returns `true` if the value exists, `false` otherwise.

- **Precondition:** The range **must be sorted** (with respect to the comparator used). Calling on an unsorted range is undefined behaviour.
- **Time complexity:** **O(log n)** — much faster than linear `find` for sorted data.
- Returns only a `bool` — it does **not** return an iterator to the found element.

**Results:**
- Search for `5` in `{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}` → `true`
- Search for `11` → `false`

**If you need the position**, use `lower_bound` or `equal_range` instead:
```cpp
auto it = std::ranges::lower_bound(sorted_for_search, 5);
// it points to the first element >= 5
```

**Related algorithms:**
| Algorithm | Returns | Description |
|-----------|---------|-------------|
| `binary_search(range, val)` | `bool` | Does the value exist? |
| `lower_bound(range, val)` | iterator | First element **≥** val |
| `upper_bound(range, val)` | iterator | First element **>** val |
| `equal_range(range, val)` | subrange | Range of elements **==** val |

**Custom comparator:**
```cpp
// Binary search on descending-sorted data
std::ranges::binary_search(vec, 5, std::greater{});
```

---

## 17. `std::ranges::nth_element` - Partial Sort / Selection

```cpp
std::vector<int> for_nth = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};
print("Before nth_element", for_nth);
std::ranges::nth_element(for_nth, for_nth.begin() + 4);
std::cout << "5th smallest element (median-ish): " << for_nth[4] << "\n";
print("After nth_element", for_nth);
```

---

```cpp
std::ranges::nth_element(for_nth, for_nth.begin() + 4);
```
Rearranges the range so that the element at the **nth position** is the element that would be there if the range were fully sorted.

- `for_nth.begin() + 4` — the **nth iterator**, pointing to index 4 (the 5th element, 0-based)
- After the call, `for_nth[4]` contains the value `5` (the 5th smallest element)
- All elements **before** index 4 are **≤ 5** (but not necessarily sorted among themselves)
- All elements **after** index 4 are **≥ 5** (but not necessarily sorted among themselves)

**Before:** `{5, 2, 8, 1, 9, 3, 7, 4, 6, 10}`
**After (one possible result):** `{3, 2, 4, 1, 5, 9, 7, 8, 6, 10}`

The only guarantee is:
1. `for_nth[4] == 5` (correct element at the nth position)
2. Everything to the left ≤ 5
3. Everything to the right ≥ 5

**Time complexity:** **O(n)** on average — significantly faster than a full sort (**O(n log n)**) when you only need one element in its correct position.

**How it works internally:**
Uses a variant of the **introselect** algorithm (quickselect with fallback to median-of-medians), which partitions around a pivot repeatedly, narrowing down to the nth position.

**Use cases:**
- Finding the **median**: `nth_element(vec, vec.begin() + vec.size() / 2)`
- Finding the **k-th smallest/largest** element
- **Top-k** problems: after `nth_element` at position k, the first k elements are the k smallest (unsorted)
- More efficient than full sort when you only need partial ordering

**Comparison with `partial_sort`:**
| Algorithm | Guarantee | Time |
|-----------|-----------|------|
| `nth_element(range, nth)` | Only the nth element is correct; left ≤ nth ≤ right | O(n) avg |
| `partial_sort(range, middle)` | Elements before `middle` are fully sorted | O(n log k) |
| `sort(range)` | Entire range sorted | O(n log n) |

---

## 18. Working with Strings - Ranges and `std::string`

```cpp
std::vector<std::string> names = {"Alice", "Bob", "Charlie", "David", "Eve"};
print("Original names", names);

std::ranges::sort(names, [](const auto& a, const auto& b) {
    return a.length() < b.length();
});
print("Sorted by length", names);
```

---

```cpp
std::vector<std::string> names = {"Alice", "Bob", "Charlie", "David", "Eve"};
```
Creates a vector of strings. Range algorithms work with **any type** that satisfies the range concept — not just integers.

---

```cpp
std::ranges::sort(names, [](const auto& a, const auto& b) {
    return a.length() < b.length();
});
```
Sorts the strings by their **length** (shortest to longest) using a custom comparator.

- `const auto&` — parameters are deduced as `const std::string&`
- `a.length() < b.length()` — compares string lengths, not lexicographic order
- The default `std::ranges::sort(names)` would sort **lexicographically** (alphabetical)

**Before:** `{"Alice", "Bob", "Charlie", "David", "Eve"}`
**After:** `{"Bob", "Eve", "Alice", "David", "Charlie"}`

**Note:** When multiple strings share the same length (e.g., "Bob" and "Eve"), their relative order is **not guaranteed** because `ranges::sort` is not stable. Use `std::ranges::stable_sort` if you need to preserve original order among equal elements.

**All range algorithms work with strings:**
```cpp
auto it = std::ranges::find(names, "Charlie");           // find by value
auto count = std::ranges::count_if(names,
    [](const auto& s) { return s.length() > 3; });       // count long names
std::ranges::reverse(names);                              // reverse the vector
```

---

## 19. Projections - Access Members Elegantly

```cpp
struct Person {
    std::string name;
    int age;
};

std::vector<Person> people = {
    {"Alice", 30}, {"Bob", 25}, {"Charlie", 35}, {"David", 28}
};

std::ranges::sort(people, {}, &Person::age);
```

---

```cpp
std::ranges::sort(people, {}, &Person::age);
```
Sorts `people` by their `age` member using a **projection**.

- `{}` — default comparator (`std::ranges::less`, ascending)
- `&Person::age` — the **projection**: a pointer-to-member that tells the algorithm to compare the `age` field instead of the entire `Person` object

This is equivalent to, but cleaner than:
```cpp
std::ranges::sort(people, [](const Person& a, const Person& b) {
    return a.age < b.age;
});
```

**Result:** People sorted by age: Bob (25), David (28), Alice (30), Charlie (35)

**What is a projection?**
A projection is the **third parameter** available on most range algorithms. It transforms each element **before** the algorithm's comparator or predicate sees it. It can be:
- A **pointer-to-member**: `&Person::age`, `&Person::name`
- A **lambda**: `[](const Person& p) { return p.age; }`
- Any **callable** that takes an element and returns a value

---

```cpp
auto person_it = std::ranges::find(people, "Charlie", &Person::name);
if (person_it != people.end()) {
    std::cout << "Found Charlie, age: " << person_it->age << "\n";
}
```
Finds a `Person` by their `name` field using a projection.

- `"Charlie"` — the value to search for
- `&Person::name` — the projection: compare `"Charlie"` against each person's `name` member
- Without projections, you'd need `find_if` with a lambda:
  ```cpp
  std::ranges::find_if(people, [](const Person& p) { return p.name == "Charlie"; });
  ```

**Projections work with almost all range algorithms:**
```cpp
// Minimum age
auto youngest = std::ranges::min(people, {}, &Person::age);

// Count people over 30
auto count = std::ranges::count_if(people,
    [](int age) { return age > 30; }, &Person::age);

// Check if all are adults
bool all_adults = std::ranges::all_of(people,
    [](int age) { return age >= 18; }, &Person::age);
```

**Why projections matter:**
- **Cleaner** than writing a full comparator lambda
- **Composable** — separate the "what to compare" from "how to compare"
- **Unique to ranges** — classic STL algorithms don't have projections

---

## 20. Combining Algorithms with Views (Range Adaptors)

```cpp
std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

auto result = data
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * x; })
    | std::views::take(3);

std::cout << "Evens -> squared -> first 3: ";
for (int x : result) {
    std::cout << x << " ";
}
```

---

```cpp
auto result = data
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * x; })
    | std::views::take(3);
```
Chains multiple **view adaptors** using the **pipe operator** `|` to build a lazy transformation pipeline.

- `std::views::filter(pred)` — keeps only elements where the predicate is `true` (even numbers: 2, 4, 6, 8, 10)
- `std::views::transform(fn)` — applies a function to each element (squares them: 4, 16, 36, 64, 100)
- `std::views::take(n)` — takes only the first `n` elements (4, 16, 36)

**Result:** `4 16 36`

**Key concept: Views are lazy.**
No computation happens when `result` is defined. The pipeline only executes when you **iterate** (e.g., in the `for` loop). Each element flows through the entire pipeline one at a time — there are no intermediate containers.

**How the pipe works:**
```
data → filter(even?) → transform(square) → take(3)
  1  →   skip        →                   →
  2  →   pass  (2)   →   4               → emit (1st)
  3  →   skip        →                   →
  4  →   pass  (4)   →   16              → emit (2nd)
  5  →   skip        →                   →
  6  →   pass  (6)   →   36              → emit (3rd) → STOP
```
Elements 7–10 are **never even examined** because `take(3)` stops after 3 results.

**Views vs Algorithms:**
| Aspect | Views (`std::views::`) | Algorithms (`std::ranges::`) |
|--------|------------------------|------------------------------|
| Execution | **Lazy** — on iteration | **Eager** — immediate |
| Memory | No intermediate copies | May produce output containers |
| Composability | Chain with `\|` | Call individually |
| Mutation | Non-mutating (read-only) | Some mutate in-place |

**Common views:**
| View | Description |
|------|-------------|
| `filter(pred)` | Keep elements matching predicate |
| `transform(fn)` | Apply function to each element |
| `take(n)` | First n elements |
| `drop(n)` | Skip first n elements |
| `reverse` | Reverse order |
| `keys` / `values` | For map-like ranges |
| `split(delim)` | Split a range by delimiter |
| `join` | Flatten nested ranges |

**Combining views with algorithms:**
```cpp
// Sort the first 3 even squares (views are read-only, so materialize first)
auto evens_squared = data
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * x; });

std::vector<int> materialized(evens_squared.begin(), evens_squared.end());
std::ranges::sort(materialized);
```

**The pipe operator `|`** is syntactic sugar. These are equivalent:
```cpp
// Pipe style
auto v = data | std::views::filter(pred) | std::views::take(3);

// Functional style
auto v = std::views::take(std::views::filter(data, pred), 3);
```

---