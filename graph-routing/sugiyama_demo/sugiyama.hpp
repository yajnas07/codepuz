// sugiyama.hpp
// Core of a minimal Sugiyama Framework: cycle removal, layer assignment,
// crossing minimization (barycenter sweep + transpose), plus ASCII and SVG
// renderers. Included by sugiyama_demo.cpp (the narrated walkthrough) and by
// sugiyama_tests.cpp (the regression testbench).
// CodePuz: codepuz.com/2026/07/crossing-minimization.html
//
// Deliberately NOT optimized for production; written to match the algorithm
// descriptions in the post one-to-one. The one concession to efficiency is the
// merge-sort inversion count in count_crossings, which is called out in the
// post as the crossings = inversions insight.

#pragma once

#include <vector>
#include <algorithm>
#include <numeric>
#include <iostream>
#include <string>
#include <unordered_map>
#include <optional>
#include <fstream>
#include <cmath>

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

// ---------------------------------------------------------------------------
// 10. SVG renderer
// ---------------------------------------------------------------------------
// Writes a standalone .svg (openable in any browser). Real nodes are labelled
// circles; dummies are small grey bend points. Edges reversed during cycle
// removal are drawn dashed/orange with the arrow pointing the forward way.

inline void render_svg(const LayeredGraph& lg, const std::string& filename,
                       const std::string& title) {
    int num_layers = static_cast<int>(lg.layers.size());
    int maxw = 0;
    for (const auto& L : lg.layers) maxw = std::max(maxw, static_cast<int>(L.size()));

    const double HS = 90, VS = 90, MX = 50, MY = 70, R = 18;
    double field = (maxw > 1 ? maxw - 1 : 0) * HS;
    double W = MX * 2 + field + 2 * R;
    double H = MY + (num_layers > 0 ? num_layers - 1 : 0) * VS + MY;

    int total = static_cast<int>(lg.layer_of.size());
    std::vector<double> X(total, 0), Y(total, 0);
    for (int L = 0; L < num_layers; ++L) {
        int k = static_cast<int>(lg.layers[L].size());
        double layer_w = (k > 1 ? k - 1 : 0) * HS;
        double start = MX + R + (field - layer_w) / 2;
        for (int p = 0; p < k; ++p) {
            int node = lg.layers[L][p];
            X[node] = start + p * HS;
            Y[node] = MY + L * VS;
        }
    }

    std::ofstream out(filename);
    if (!out) { std::cerr << "  could not write " << filename << "\n"; return; }

    auto is_dummy = [&](int node) {
        return node < static_cast<int>(lg.labels.size()) && lg.labels[node] == "_";
    };

    out << "<?xml version='1.0' encoding='UTF-8'?>\n"
        << "<svg xmlns='http://www.w3.org/2000/svg' width='" << W << "' height='" << H
        << "' viewBox='0 0 " << W << " " << H << "'>\n"
        << "<defs><marker id='arrow' markerWidth='9' markerHeight='9' refX='7' refY='3' "
           "orient='auto'><path d='M0,0 L7,3 L0,6 Z' fill='#555'/></marker></defs>\n"
        << "<rect width='100%' height='100%' fill='white'/>\n"
        << "<text x='" << (W / 2) << "' y='30' font-family='sans-serif' font-size='18' "
           "text-anchor='middle' font-weight='bold'>" << title << "</text>\n";

    // Edges (drawn first, under the nodes).
    for (const auto& e : lg.edges) {
        double x1 = X[e.from], y1 = Y[e.from], x2 = X[e.to], y2 = Y[e.to];
        double dx = x2 - x1, dy = y2 - y1, len = std::sqrt(dx * dx + dy * dy);
        double ux = len > 0 ? dx / len : 0, uy = len > 0 ? dy / len : 0;
        // Pull endpoints off real-node circles so the arrow sits on the rim.
        if (!is_dummy(e.from)) { x1 += ux * R; y1 += uy * R; }
        bool to_real = !is_dummy(e.to);
        if (to_real) { x2 -= ux * R; y2 -= uy * R; }
        std::string color = e.reversed ? "#d9822b" : "#888";
        out << "<line x1='" << x1 << "' y1='" << y1 << "' x2='" << x2 << "' y2='" << y2
            << "' stroke='" << color << "' stroke-width='1.8'"
            << (e.reversed ? " stroke-dasharray='6,4'" : "")
            << (to_real ? " marker-end='url(#arrow)'" : "") << "/>\n";
    }

    // Nodes.
    for (int node = 0; node < total; ++node) {
        if (is_dummy(node)) {
            out << "<circle cx='" << X[node] << "' cy='" << Y[node]
                << "' r='3.5' fill='#bbb'/>\n";
            continue;
        }
        const std::string& lab = (node < static_cast<int>(lg.labels.size()))
                                 ? lg.labels[node] : std::string("?");
        out << "<circle cx='" << X[node] << "' cy='" << Y[node] << "' r='" << R
            << "' fill='#dceaf7' stroke='#2c6fb0' stroke-width='2'/>\n"
            << "<text x='" << X[node] << "' y='" << (Y[node] + 5)
            << "' font-family='sans-serif' font-size='15' text-anchor='middle'>"
            << lab << "</text>\n";
    }

    out << "</svg>\n";
    std::cout << "  wrote " << filename << "\n";
}

// ---------------------------------------------------------------------------
// 11. Circular renderer for a plain (possibly cyclic) Graph
// ---------------------------------------------------------------------------
// Before layering there is no top-to-bottom structure, so we draw the raw graph
// with nodes placed evenly on a circle and edges as gently bowed arcs. This is
// the canonical way to show an arbitrary directed graph and makes cycles easy
// to see. `highlight[i] == true` draws edge i dashed/orange (e.g. the cycle's
// back edges, or the edges reversed by cycle removal).

inline void render_svg_circular(const Graph& g, const std::string& filename,
                                const std::string& title,
                                const std::vector<bool>& highlight = {}) {
    const double PI = 3.14159265358979323846;
    const double R = 20;                             // node radius
    const double PAD = 60;                           // margin around the ring
    double ring = std::max(120.0, g.n * 26.0);       // ring radius scales with n
    double cx = PAD + ring + R;
    double cy = PAD + ring + R + 24;                 // leave room for the title
    double W = 2 * (PAD + ring + R);
    double H = W + 24;

    std::vector<double> X(g.n), Y(g.n);
    for (int i = 0; i < g.n; ++i) {
        double ang = -PI / 2 + 2 * PI * i / (g.n > 0 ? g.n : 1); // node 0 at top
        X[i] = cx + ring * std::cos(ang);
        Y[i] = cy + ring * std::sin(ang);
    }

    std::ofstream out(filename);
    if (!out) { std::cerr << "  could not write " << filename << "\n"; return; }

    out << "<?xml version='1.0' encoding='UTF-8'?>\n"
        << "<svg xmlns='http://www.w3.org/2000/svg' width='" << W << "' height='" << H
        << "' viewBox='0 0 " << W << " " << H << "'>\n"
        << "<defs>"
           "<marker id='arrow' markerWidth='9' markerHeight='9' refX='7' refY='3' "
           "orient='auto'><path d='M0,0 L7,3 L0,6 Z' fill='#666'/></marker>"
           "<marker id='arrowh' markerWidth='9' markerHeight='9' refX='7' refY='3' "
           "orient='auto'><path d='M0,0 L7,3 L0,6 Z' fill='#d9822b'/></marker>"
           "</defs>\n"
        << "<rect width='100%' height='100%' fill='white'/>\n"
        << "<text x='" << (W / 2) << "' y='28' font-family='sans-serif' font-size='18' "
           "text-anchor='middle' font-weight='bold'>" << title << "</text>\n";

    // Edges: bowed quadratic arcs so opposite edges don't overlap and arcs
    // avoid passing straight through the node at the circle's centre.
    for (std::size_t i = 0; i < g.edges.size(); ++i) {
        const Edge& e = g.edges[i];
        bool hi = i < highlight.size() && highlight[i];
        double x1 = X[e.from], y1 = Y[e.from], x2 = X[e.to], y2 = Y[e.to];
        double dx = x2 - x1, dy = y2 - y1, len = std::sqrt(dx * dx + dy * dy);
        if (len < 1e-9) continue;
        double ux = dx / len, uy = dy / len;
        x1 += ux * R; y1 += uy * R;          // start on source rim
        x2 -= ux * R; y2 -= uy * R;          // end on target rim (room for arrow)
        double mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
        double off = 0.15 * len;             // consistent left-hand bow
        double px = mx + (-uy) * off, py = my + (ux) * off;
        out << "<path d='M" << x1 << "," << y1 << " Q" << px << "," << py << " "
            << x2 << "," << y2 << "' fill='none' stroke='"
            << (hi ? "#d9822b" : "#888") << "' stroke-width='1.8'"
            << (hi ? " stroke-dasharray='6,4'" : "")
            << " marker-end='url(#" << (hi ? "arrowh" : "arrow") << ")'/>\n";
    }

    // Nodes.
    for (int i = 0; i < g.n; ++i) {
        const std::string& lab = (i < static_cast<int>(g.labels.size()))
                                 ? g.labels[i] : std::to_string(i);
        out << "<circle cx='" << X[i] << "' cy='" << Y[i] << "' r='" << R
            << "' fill='#dceaf7' stroke='#2c6fb0' stroke-width='2'/>\n"
            << "<text x='" << X[i] << "' y='" << (Y[i] + 5)
            << "' font-family='sans-serif' font-size='15' text-anchor='middle'>"
            << lab << "</text>\n";
    }

    out << "</svg>\n";
    std::cout << "  wrote " << filename << "\n";
}
