// sugiyama_demo.cpp
// Narrated walkthrough of the Sugiyama framework on a single 10-node directed
// graph that contains a cycle. It prints the input graph, then runs each stage
// of the pipeline in turn, showing (ASCII in the terminal + an .svg file) how
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

#include "sugiyama.hpp"
#include <random>
#include <set>
#include <cstdlib>

// Keep the input small so the (polynomial but not free) minimization stays fast
// and the diagrams stay readable.
static const int MAX_NODES = 15;
static const int MAX_EDGES = 30;

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
    render_svg_circular(g, "step0_input.svg", "Step 0: input graph (with cycle)",
                        back_edge_mask(g));
    std::cout << "  (circular layout; dashed orange edge closes the cycle)\n\n";

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
    {
        // Same circular layout; the reversed edge is now dashed orange and
        // points the new (forward) way.
        std::vector<bool> rev(g.edges.size());
        for (std::size_t i = 0; i < g.edges.size(); ++i) rev[i] = g.edges[i].reversed;
        render_svg_circular(g, "step1_dag.svg", "Step 1: after cycle removal (DAG)", rev);
        std::cout << "  (same layout; reversed edge now dashed orange, pointing the new way)\n\n";
    }

    // --- Step 2: layer assignment + dummy nodes ---------------------------
    std::cout << "STEP 2 - layer assignment (longest path) + dummy nodes for long edges\n";
    LayeredGraph lg = assign_layers(g);
    int n_dummies = static_cast<int>(lg.layer_of.size()) - lg.n_real;
    std::cout << "  layers: " << lg.layers.size()
              << ",  dummy nodes inserted: " << n_dummies << "\n\n";
    render_ascii(lg, "STEP 2 - after layer assignment (dots = dummy bend points)");
    render_svg(lg, "step2_layers.svg", "Step 2: layer assignment + dummies");
    std::cout << "\n";

    // --- Step 3: crossing minimization ------------------------------------
    std::cout << "STEP 3 - crossing minimization (barycenter sweeps + transpose)\n\n";
    render_ascii(lg, "STEP 3a - initial order, before minimization");

    barycenter_sweep(lg, 0);
    render_ascii(lg, "STEP 3b - after one left-to-right barycenter sweep");
    render_svg(lg, "step3_sweep.svg", "Step 3: after one barycenter sweep");
    std::cout << "\n";

    minimize_crossings(lg);

    // --- Final ------------------------------------------------------------
    render_ascii(lg, "FINAL - minimized layered layout");
    render_svg(lg, "final_layout.svg", "Final: minimized layered layout");


    std::cout << "\nWrote SVGs: step0_input.svg, step1_dag.svg, step2_layers.svg,\n"
                 "            step3_sweep.svg, final_layout.svg  (open any in a browser)\n";
    return 0;
}
