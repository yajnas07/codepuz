// sugiyama_tests.cpp
// Regression testbench for the Sugiyama framework (sugiyama.hpp).
// Three fixtures: a small A-F DAG, a 4-node cyclic graph, and a 10-node graph.
//
// Compile: g++ -std=c++17 -O2 sugiyama_tests.cpp -o sugiyama_tests

#include "sugiyama.hpp"

static Graph make_af_graph() {
    Graph g;
    g.labels = {"A","B","C","D","E","F"};   // ids 0..5
    g.n = 6;
    auto id = [&](const std::string& s){
        return static_cast<int>(std::find(g.labels.begin(), g.labels.end(), s)
                                - g.labels.begin());
    };
    std::vector<std::pair<std::string,std::string>> es = {
        {"A","C"},{"A","D"},{"B","C"},{"B","E"},{"C","F"},{"D","F"},{"E","F"}
    };
    for (auto& p : es) g.edges.push_back({id(p.first), id(p.second)});
    return g;
}

int main() {
    // === Test 1: A-F graph ===
    std::cout << "=== Test 1: A-F Graph ===\n";
    {
        Graph g = make_af_graph();
        std::cout << "Has cycle: " << (has_cycle(g) ? "yes" : "no") << "\n";
        LayeredGraph lg = assign_layers(g);
        std::cout << "After layer assignment: " << total_crossings(lg) << "\n";
        barycenter_sweep(lg, 0);
        std::cout << "After 1 barycenter sweep: " << total_crossings(lg) << "\n";
        minimize_crossings(lg);
        std::cout << "After full minimization: " << total_crossings(lg) << "\n";
        std::cout << "Final layout:\n";
        print_layout(lg, g);
        render_ascii(lg, "Test 1 - final layout");
    }

    // === Test 2: cyclic graph (P,Q,R,S) ===
    std::cout << "\n=== Test 2: Cyclic Graph (cycle removal) ===\n";
    {
        Graph g;
        g.labels = {"P","Q","R","S"};
        g.n = 4;
        g.edges = { {0,1},{1,2},{2,0},{0,3},{3,1} }; // P->Q Q->R R->P P->S S->Q
        std::cout << "Has cycle before: " << (has_cycle(g) ? "yes" : "no") << "\n";
        remove_cycles(g);
        std::cout << "Has cycle after:  " << (has_cycle(g) ? "yes" : "no") << "\n";
        std::cout << "Reversed edges:";
        for (const auto& e : g.edges)
            if (e.reversed)
                std::cout << " " << g.labels[e.to] << "->" << g.labels[e.from]
                          << "(now " << g.labels[e.from] << "->" << g.labels[e.to] << ")";
        std::cout << "\n";
        LayeredGraph lg = assign_layers(g);
        minimize_crossings(lg);
        std::cout << "Layout after removal + minimization:\n";
        print_layout(lg, g);
        render_ascii(lg, "Test 2 - final layout");
    }

    // === Test 3: random-ish 10-node graph ===
    std::cout << "\n=== Test 3: 10-node Graph ===\n";
    {
        Graph g;
        g.n = 10;
        for (int i = 0; i < 10; ++i) g.labels.push_back(std::string(1, char('0'+i)));
        // Fixed edge set (DAG, forward by construction) for reproducibility.
        std::vector<std::pair<int,int>> es = {
            {0,2},{0,3},{1,3},{1,4},{2,5},{3,5},{3,6},{4,6},
            {5,7},{6,7},{6,8},{7,9},{8,9},{2,6},{0,5}
        };
        for (auto& p : es) g.edges.push_back({p.first, p.second});
        LayeredGraph lg = assign_layers(g);
        int before = total_crossings(lg);
        minimize_crossings(lg);
        int after = total_crossings(lg);
        std::cout << "Crossings before: " << before << ", after: " << after << "\n";
        print_layout(lg, g);
        render_ascii(lg, "Test 3 - final layout");
    }
    return 0;
}
