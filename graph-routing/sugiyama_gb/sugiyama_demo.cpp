// sugiyama_demo.cpp
// SIngle file version of the Sugiyama framework on a single 10-node directed
// graph that contains a cycle. It prints the input graph, then runs each stage
// of the pipeline in turn, showing (ASCII in the terminal) how
// the drawing changes at every step, and finally the minimized layout.
//
// The algorithm itself lives in sugiyama.hpp; the regression testbench lives in
// sugiyama_tests.cpp.
//
// Compile: g++ -std=c++17 -O2 sugiyama_demo.cpp -o sugiyama_demo
// ./sugiyama_demo                    # built-in 10-node demo graph
// ./sugiyama_demo <nodes> <edges>    # random graph
// ./sugiyama_demo <nodes> <edges> <seed>   # reproducible random graph
// For Example:  ./sugiyama_demo.exe 6 15
// CodePuz: codepuz.com/2026/07/crossing-minimization.html

#include <random>
#include <set>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iostream>
#include <string>
#include <unordered_map>
#include <optional>
#include <fstream>
#include <cmath>


// Keep the input small so the (polynomial but not free) minimization stays fast
// and the diagrams stay readable.
static const int MAX_NODES = 15;
static const int MAX_EDGES = 30;

// ---------------------------------------------------------------------------
// Data structures
// ---------------------------------------------------------------------------

struct Edge {
    int from, to;
    bool reversed = false;   // set true if reversed during cycle removal
};

struct Graph {
    int n;                                // number of real nodes
    std::vector<Edge> edges;
    std::vector<std::string> labels;      // node display names, size n
};

struct LayeredGraph {
    std::vector<std::vector<int>> layers; // layers[i] = ordered node IDs in layer i
    std::vector<int> layer_of;            // layer_of[node] = layer index
    std::vector<Edge> edges;              // includes dummy-chain edges
    int n_real = 0;                       // count of real (non-dummy) nodes
    std::vector<std::string> labels;      // labels[node]; dummies get empty/∅

    // position of a node within its own layer (index in layers[layer_of[node]])
    std::vector<int> pos;

    void recompute_positions() {
        int max_id = static_cast<int>(layer_of.size());
        pos.assign(max_id, -1);
        for (auto& layer : layers)
            for (int i = 0; i < static_cast<int>(layer.size()); ++i)
                pos[layer[i]] = i;
    }
};

// ---------------------------------------------------------------------------
// 1. Cycle detection (DFS, grey/white/black coloring)
// ---------------------------------------------------------------------------
// White = 0 (unvisited), Grey = 1 (on current DFS stack), Black = 2 (done).
// A grey -> grey edge is a back edge, i.e. a cycle.

inline bool dfs_find_back_edge(int u,
                               const std::vector<std::vector<int>>& adj,
                               std::vector<int>& color,
                               std::optional<std::pair<int,int>>& back) {
    color[u] = 1; // grey
    for (int v : adj[u]) {
        if (color[v] == 0) {
            if (dfs_find_back_edge(v, adj, color, back)) return true;
        } else if (color[v] == 1) {
            back = std::make_pair(u, v); // grey -> grey: back edge
            return true;
        }
    }
    color[u] = 2; // black
    return false;
}

inline std::optional<std::pair<int,int>> find_one_back_edge(const Graph& g) {
    std::vector<std::vector<int>> adj(g.n);
    for (const auto& e : g.edges) adj[e.from].push_back(e.to);

    std::vector<int> color(g.n, 0);
    std::optional<std::pair<int,int>> back;
    for (int s = 0; s < g.n; ++s) {
        if (color[s] == 0) {
            if (dfs_find_back_edge(s, adj, color, back)) return back;
        }
    }
    return std::nullopt;
}

inline bool has_cycle(const Graph& g) {
    return find_one_back_edge(g).has_value();
}

// ---------------------------------------------------------------------------
// 2. Cycle removal (greedy: reverse the first back edge found, repeat)
// ---------------------------------------------------------------------------

inline void remove_cycles(Graph& g) {
    while (auto back = find_one_back_edge(g)) {
        int fu = back->first, fv = back->second;
        for (auto& e : g.edges) {
            if (e.from == fu && e.to == fv && !e.reversed) {
                std::swap(e.from, e.to);   // reverse direction
                e.reversed = true;
                break;
            }
        }
    }
}

// ---------------------------------------------------------------------------
// 3. Layer assignment (longest path) + dummy node insertion
// ---------------------------------------------------------------------------
// Assumes g is already a DAG (call remove_cycles first).
// layer(v) = max over predecessors u of (layer(u) + 1); sources get 0.

inline LayeredGraph assign_layers(const Graph& g) {
    LayeredGraph lg;
    lg.n_real = g.n;

    std::vector<std::vector<int>> adj(g.n);
    std::vector<int> indeg(g.n, 0);
    for (const auto& e : g.edges) {
        adj[e.from].push_back(e.to);
        indeg[e.to]++;
    }

    // Kahn topological order.
    std::vector<int> topo, layer(g.n, 0);
    std::vector<int> q;
    for (int i = 0; i < g.n; ++i) if (indeg[i] == 0) q.push_back(i);
    std::sort(q.begin(), q.end()); // deterministic source order
    for (std::size_t i = 0; i < q.size(); ++i) {
        int u = q[i];
        topo.push_back(u);
        std::vector<int> newly;
        for (int v : adj[u]) {
            layer[v] = std::max(layer[v], layer[u] + 1);
            if (--indeg[v] == 0) newly.push_back(v);
        }
        std::sort(newly.begin(), newly.end());
        for (int v : newly) q.push_back(v);
    }

    int num_layers = 0;
    for (int i = 0; i < g.n; ++i) num_layers = std::max(num_layers, layer[i] + 1);

    lg.labels = g.labels;
    lg.layer_of = layer;

    // Insert dummy nodes for edges spanning more than one layer.
    // A real edge u->v with layer(v) - layer(u) > 1 becomes a chain
    // u -> d1 -> d2 -> ... -> v with one dummy per intermediate layer.
    int next_id = g.n;
    for (const auto& e : g.edges) {
        int lu = layer[e.from], lv = layer[e.to];
        if (lv - lu <= 1) {
            lg.edges.push_back(e);
            continue;
        }
        int prev = e.from;
        for (int L = lu + 1; L < lv; ++L) {
            int d = next_id++;
            lg.labels.push_back("_"); // dummy marker; rendered as ∅ / invisible
            lg.layer_of.push_back(L);
            Edge seg; seg.from = prev; seg.to = d; seg.reversed = e.reversed;
            lg.edges.push_back(seg);
            prev = d;
        }
        Edge last; last.from = prev; last.to = e.to; last.reversed = e.reversed;
        lg.edges.push_back(last);
    }

    // Build layer buckets in deterministic initial order (by node ID).
    lg.layers.assign(num_layers, {});
    int total = static_cast<int>(lg.layer_of.size());
    for (int node = 0; node < total; ++node)
        lg.layers[lg.layer_of[node]].push_back(node);
    for (auto& layer_bucket : lg.layers)
        std::sort(layer_bucket.begin(), layer_bucket.end());

    lg.recompute_positions();
    return lg;
}

// ---------------------------------------------------------------------------
// 4. Crossing count between layer_idx and layer_idx+1
// ---------------------------------------------------------------------------
// Insight (used in the post): sort the edges by source position, then the
// number of crossings equals the number of inversions in the sequence of
// destination positions. Count inversions with merge sort in O(E log E).

inline long long count_inversions(std::vector<int>& a) {
    if (a.size() <= 1) return 0;
    std::size_t mid = a.size() / 2;
    std::vector<int> left(a.begin(), a.begin() + mid);
    std::vector<int> right(a.begin() + mid, a.end());
    long long inv = count_inversions(left) + count_inversions(right);
    std::size_t i = 0, j = 0, k = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] <= right[j]) {
            a[k++] = left[i++];
        } else {
            a[k++] = right[j++];
            inv += static_cast<long long>(left.size() - i); // all remaining left > right[j]
        }
    }
    while (i < left.size())  a[k++] = left[i++];
    while (j < right.size()) a[k++] = right[j++];
    return inv;
}

inline int count_crossings(const LayeredGraph& lg, int layer_idx) {
    // Gather edges from layer_idx to layer_idx+1 as (src_pos, dst_pos) pairs.
    std::vector<std::pair<int,int>> segs;
    for (const auto& e : lg.edges) {
        if (lg.layer_of[e.from] == layer_idx && lg.layer_of[e.to] == layer_idx + 1)
            segs.push_back({lg.pos[e.from], lg.pos[e.to]});
    }
    // Sort by source position; ties broken by destination position so that
    // two edges sharing a source do not count as a crossing among themselves.
    std::sort(segs.begin(), segs.end());
    std::vector<int> dst;
    dst.reserve(segs.size());
    for (auto& s : segs) dst.push_back(s.second);
    return static_cast<int>(count_inversions(dst));
}

inline int total_crossings(const LayeredGraph& lg) {
    int total = 0;
    for (int L = 0; L + 1 < static_cast<int>(lg.layers.size()); ++L)
        total += count_crossings(lg, L);
    return total;
}

// ---------------------------------------------------------------------------
// 5. Barycenter sweep
// ---------------------------------------------------------------------------
// direction = 0: left-to-right. Layer L's ordering fixed, reorder layer L+1.
// direction = 1: right-to-left. Layer L+1's ordering fixed, reorder layer L.
// Barycenter of a node = mean position of its neighbors in the fixed layer.
// Nodes with no neighbor in the fixed layer keep their current position.
// Ties broken by current index via std::stable_sort.

inline void barycenter_sweep(LayeredGraph& lg, int direction) {
    int num = static_cast<int>(lg.layers.size());
    lg.recompute_positions();

    auto reorder = [&](int fixed_layer, int target_layer) {
        std::vector<std::pair<double,int>> keyed; // (barycenter, node)
        for (int node : lg.layers[target_layer]) {
            double sum = 0.0; int cnt = 0;
            for (const auto& e : lg.edges) {
                if (e.from == node && lg.layer_of[e.to] == fixed_layer) {
                    sum += lg.pos[e.to]; ++cnt;
                }
                if (e.to == node && lg.layer_of[e.from] == fixed_layer) {
                    sum += lg.pos[e.from]; ++cnt;
                }
            }
            double bary = (cnt > 0) ? sum / cnt
                                    : static_cast<double>(lg.pos[node]);
            keyed.push_back({bary, node});
        }
        std::stable_sort(keyed.begin(), keyed.end(),
                         [](const auto& a, const auto& b){ return a.first < b.first; });
        for (std::size_t i = 0; i < keyed.size(); ++i)
            lg.layers[target_layer][i] = keyed[i].second;
        lg.recompute_positions();
    };

    if (direction == 0) {
        for (int L = 0; L + 1 < num; ++L) reorder(L, L + 1);
    } else {
        for (int L = num - 1; L - 1 >= 0; --L) reorder(L, L - 1);
    }
}

// ---------------------------------------------------------------------------
// 6. Transpose: local search, swap adjacent nodes if it reduces crossings
// ---------------------------------------------------------------------------

inline bool transpose(LayeredGraph& lg, int layer_idx) {
    bool improved = false;
    auto& layer = lg.layers[layer_idx];
    for (int i = 0; i + 1 < static_cast<int>(layer.size()); ++i) {
        // crossings affected by this layer touch pair (layer_idx-1, layer_idx)
        // and (layer_idx, layer_idx+1).
        auto local = [&]() {
            int c = 0;
            if (layer_idx > 0) c += count_crossings(lg, layer_idx - 1);
            if (layer_idx + 1 < static_cast<int>(lg.layers.size()))
                c += count_crossings(lg, layer_idx);
            return c;
        };
        lg.recompute_positions();
        int before = local();
        std::swap(layer[i], layer[i + 1]);
        lg.recompute_positions();
        int after = local();
        if (after < before) {
            improved = true;           // keep the swap
        } else {
            std::swap(layer[i], layer[i + 1]); // revert
            lg.recompute_positions();
        }
    }
    return improved;
}

// ---------------------------------------------------------------------------
// 7. Outer minimization loop
// ---------------------------------------------------------------------------

inline void minimize_crossings(LayeredGraph& lg, int max_iter = 24) {
    auto snapshot = lg.layers;
    int best = total_crossings(lg);

    for (int iter = 0; iter < max_iter; ++iter) {
        barycenter_sweep(lg, iter % 2);            // alternate LTR / RTL
        bool any = false;
        for (int L = 0; L < static_cast<int>(lg.layers.size()); ++L)
            any |= transpose(lg, L);

        int cur = total_crossings(lg);
        if (cur < best) { best = cur; snapshot = lg.layers; }
        if (cur == 0) break;
        if (!any && iter % 2 == 1) { /* stable-ish; keep iterating to max */ }
    }

    lg.layers = snapshot;   // restore best-seen layout
    lg.recompute_positions();
}

// ---------------------------------------------------------------------------
// 8. Pretty printer
// ---------------------------------------------------------------------------

inline void print_layout(const LayeredGraph& lg, const Graph& /*original*/) {
    for (int L = 0; L < static_cast<int>(lg.layers.size()); ++L) {
        std::cout << "  Layer " << L << ":";
        for (int node : lg.layers[L]) {
            const std::string& lab = (node < static_cast<int>(lg.labels.size()))
                                     ? lg.labels[node] : std::string("?");
            std::cout << " " << (lab == "_" ? "ø" : lab); // ø for dummy
        }
        std::cout << "\n";
    }
    std::cout << "Crossings per layer pair: [";
    for (int L = 0; L + 1 < static_cast<int>(lg.layers.size()); ++L) {
        std::cout << count_crossings(lg, L);
        if (L + 2 < static_cast<int>(lg.layers.size())) std::cout << ", ";
    }
    std::cout << "]\n";
}

// ---------------------------------------------------------------------------
// 9. ASCII-art renderer
// ---------------------------------------------------------------------------
// Layers stacked top-to-bottom, nodes centered within each layer, edges
// approximated with / | \ across the rows between adjacent layers.
// Dummy nodes (label "_") render as a small '.' bend point.
// Assumes lg.pos is current (the pipeline recomputes it at every stage).
// show_metrics=false suppresses the crossing count (meaningless before the
// graph is properly layered, e.g. the raw input / pre-dummy views).

inline void render_ascii(const LayeredGraph& lg, const std::string& title,
                         bool show_metrics = true) {
    int num_layers = static_cast<int>(lg.layers.size());
    int maxw = 0;
    for (const auto& L : lg.layers) maxw = std::max(maxw, static_cast<int>(L.size()));

    const int COL = 6;   // horizontal slot width per node
    const int ROW = 4;   // rows between adjacent layers
    int W = std::max(1, maxw) * COL + 2;
    int H = (num_layers > 0 ? (num_layers - 1) * ROW : 0) + 1;

    std::vector<std::string> canvas(H, std::string(W, ' '));
    auto put = [&](int r, int c, char ch) {
        if (r >= 0 && r < H && c >= 0 && c < W) canvas[r][c] = ch;
    };

    // Canvas coordinate of every placed node.
    int total = static_cast<int>(lg.layer_of.size());
    std::vector<int> cx(total, -1), cy(total, -1);
    for (int L = 0; L < num_layers; ++L) {
        int k = static_cast<int>(lg.layers[L].size());
        int start = (W - k * COL) / 2;
        for (int p = 0; p < k; ++p) {
            int node = lg.layers[L][p];
            cx[node] = start + p * COL + COL / 2;
            cy[node] = L * ROW;
        }
    }

    // Edges first, so node glyphs overwrite line chars at the endpoints.
    for (const auto& e : lg.edges) {
        int top = e.from, bot = e.to;
        if (lg.layer_of[top] > lg.layer_of[bot]) std::swap(top, bot);
        if (cx[top] < 0 || cx[bot] < 0) continue;
        int r1 = cy[top], c1 = cx[top], r2 = cy[bot], c2 = cx[bot];
        if (r2 == r1) continue;
        for (int r = r1 + 1; r < r2; ++r) {
            double t = static_cast<double>(r - r1) / (r2 - r1);
            int c = static_cast<int>(std::lround(c1 + t * (c2 - c1)));
            put(r, c, (c2 > c1) ? '\\' : (c2 < c1) ? '/' : '|');
        }
    }

    // Nodes.
    for (int node = 0; node < total; ++node) {
        if (cx[node] < 0) continue;
        const std::string& lab = (node < static_cast<int>(lg.labels.size()))
                                 ? lg.labels[node] : std::string("?");
        if (lab == "_") {
            put(cy[node], cx[node], '.');   // dummy bend point
        } else {
            int c0 = cx[node] - static_cast<int>(lab.size()) / 2;
            for (int i = 0; i < static_cast<int>(lab.size()); ++i)
                put(cy[node], c0 + i, lab[i]);
        }
    }

    std::cout << title << "\n";
    for (auto& row : canvas) {
        int last = static_cast<int>(row.size());
        while (last > 0 && row[last - 1] == ' ') --last;
        std::cout << row.substr(0, last) << "\n";
    }
    if (show_metrics)
        std::cout << "  crossings = " << total_crossings(lg) << "\n";
    std::cout << "\n";
}




// A 10-node directed graph. Mostly a DAG, plus one back edge (8 -> 3) that
// closes the cycle 3 -> 6 -> 8 -> 3, so the cycle-removal stage has work to do.
static Graph make_demo_graph() {
    Graph g;
    g.n = 10;
    for (int i = 0; i < 10; ++i) g.labels.push_back(std::to_string(i));
    std::vector<std::pair<int,int>> es = {
        {0,2},{0,3},{1,3},{1,4},{2,5},{3,5},{3,6},{4,6},
        {5,7},{6,7},{6,8},{7,9},{8,9},{2,6},{0,5},
        {8,3}   // back edge: closes the cycle 3 -> 6 -> 8 -> 3
    };
    for (auto& p : es) g.edges.push_back({p.first, p.second});
    return g;
}

// Build a random directed graph with `n` nodes and `m` distinct edges
// (no self-loops, no duplicate edges). Cycles may occur naturally, which is
// exactly what makes the pipeline interesting. Deterministic for a given seed.
static Graph make_random_graph(int n, int m, unsigned seed) {
    Graph g;
    g.n = n;
    for (int i = 0; i < n; ++i) g.labels.push_back(std::to_string(i));

    std::mt19937 rng(seed);
    std::uniform_int_distribution<int> pick(0, n - 1);
    std::set<std::pair<int,int>> used;

    // Cap at what a simple digraph without anti-parallel pairs can hold: at most
    // one of u->v / v->u per node pair, so n*(n-1)/2 edges.
    long long max_possible = static_cast<long long>(n) * (n - 1) / 2;
    if (m > max_possible) m = static_cast<int>(max_possible);

    int guard = m * 50 + 100;   // bail out if we somehow can't find new edges
    while (static_cast<int>(g.edges.size()) < m && guard-- > 0) {
        int u = pick(rng), v = pick(rng);
        if (u == v) continue;                       // no self-loops
        if (used.count({u, v}) || used.count({v, u})) continue; // no dup / anti-parallel
        used.insert({u, v});
        g.edges.push_back({u, v});
    }
    return g;
}

// Which edges close a cycle: reverse a copy and see which ones flipped.
// remove_cycles reverses edges in place, so indices line up with the original.
static std::vector<bool> back_edge_mask(const Graph& g) {
    Graph c = g;
    remove_cycles(c);
    std::vector<bool> mask(g.edges.size(), false);
    for (std::size_t i = 0; i < c.edges.size(); ++i)
        mask[i] = c.edges[i].reversed;
    return mask;
}

// Adjacency-list view: one line per node listing its out-neighbours in the
// current edge directions (so it reflects any edges flipped by cycle removal).
static void print_adjacency(const Graph& g, const std::string& title) {
    std::vector<std::vector<int>> adj(g.n);
    for (const auto& e : g.edges) adj[e.from].push_back(e.to);
    std::cout << title << "\n";
    for (int u = 0; u < g.n; ++u) {
        std::cout << "  " << g.labels[u] << " ->";
        if (adj[u].empty()) {
            std::cout << " (none)";
        } else {
            for (std::size_t i = 0; i < adj[u].size(); ++i)
                std::cout << (i ? "," : "") << " " << g.labels[adj[u][i]];
        }
        std::cout << "\n";
    }
    std::cout << "\n";
}

static void print_edge_list(const Graph& g, const std::string& title) {
    std::cout << title << "\n  nodes:";
    for (int i = 0; i < g.n; ++i) std::cout << " " << g.labels[i];
    std::cout << "\n  edges:";
    for (std::size_t i = 0; i < g.edges.size(); ++i) {
        const auto& e = g.edges[i];
        std::cout << " " << g.labels[e.from] << "->" << g.labels[e.to];
    }
    std::cout << "\n\n";
}

int main(int argc, char** argv) {
    std::cout << "==========================================================\n"
                 " Sugiyama layered graph drawing - pipeline walkthrough\n"
                 "==========================================================\n\n";

    // --- Input -------------------------------------------------------------
    // Optional args: <nodes> <edges> [seed]. With no args, use the built-in
    // demo graph. Sizes are capped at MAX_NODES / MAX_EDGES to keep it fast.
    Graph g;
    if (argc >= 3) {
        int n = std::atoi(argv[1]);
        int m = std::atoi(argv[2]);
        if (n < 2) { std::cout << "note: raising nodes to the minimum of 2\n"; n = 2; }
        if (n > MAX_NODES) { std::cout << "note: capping nodes at " << MAX_NODES << "\n"; n = MAX_NODES; }
        if (m < 1) { std::cout << "note: raising edges to the minimum of 1\n"; m = 1; }
        if (m > MAX_EDGES) { std::cout << "note: capping edges at " << MAX_EDGES << "\n"; m = MAX_EDGES; }

        unsigned seed = (argc >= 4)
            ? static_cast<unsigned>(std::strtoul(argv[3], nullptr, 10))
            : std::random_device{}();
        std::cout << "Random graph: nodes=" << n << ", edges=" << m
                  << ", seed=" << seed << " (re-run with this seed to reproduce)\n\n";
        g = make_random_graph(n, m, seed);
    } else {
        std::cout << "Usage: " << argv[0] << " [nodes<=" << MAX_NODES
                  << "] [edges<=" << MAX_EDGES << "] [seed]\n"
                  << "No args given -> using the built-in 10-node demo graph.\n\n";
        g = make_demo_graph();
    }

    print_edge_list(g, "INPUT: a " + std::to_string(g.n)
                         + "-node directed graph (" + std::to_string(g.edges.size()) + " edges)");
    std::cout << "Cycle present? " << (has_cycle(g) ? "yes" : "no") << "\n\n";

    print_adjacency(g, "STEP 0 - input graph (adjacency list)");
    // Draw the raw input as a circular layout (no layers yet). The dashed
    // orange edge is the one that closes the cycle.


    // --- Step 1: cycle removal --------------------------------------------
    std::cout << "STEP 1 - cycle removal: reverse back edges to obtain a DAG\n";
    remove_cycles(g);
    std::cout << "  reversed edges:";
    for (const auto& e : g.edges)
        if (e.reversed)
            std::cout << " " << g.labels[e.from] << "->" << g.labels[e.to]
                      << " (originally " << g.labels[e.to] << "->" << g.labels[e.from] << ")";
    std::cout << "\n  cycle present now? " << (has_cycle(g) ? "yes" : "no") << "\n\n";
    print_adjacency(g, "STEP 1 - after cycle removal (adjacency list)");
    
    // --- Step 2: layer assignment + dummy nodes ---------------------------
    std::cout << "STEP 2 - layer assignment (longest path) + dummy nodes for long edges\n";
    LayeredGraph lg = assign_layers(g);
    int n_dummies = static_cast<int>(lg.layer_of.size()) - lg.n_real;
    std::cout << "  layers: " << lg.layers.size()
              << ",  dummy nodes inserted: " << n_dummies << "\n\n";
    render_ascii(lg, "STEP 2 - after layer assignment (dots = dummy bend points)");
    std::cout << "\n";

    // --- Step 3: crossing minimization ------------------------------------
    std::cout << "STEP 3 - crossing minimization (barycenter sweeps + transpose)\n\n";
    render_ascii(lg, "STEP 3a - initial order, before minimization");

    barycenter_sweep(lg, 0);
    render_ascii(lg, "STEP 3b - after one left-to-right barycenter sweep");
 
    std::cout << "\n";

    minimize_crossings(lg);

    // --- Final ------------------------------------------------------------
    render_ascii(lg, "FINAL - minimized layered layout");
 

 
    return 0;
}
