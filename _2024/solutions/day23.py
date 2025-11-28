"""Day 23: LAN Party

This module provides the solution for Advent of Code 2024 - Day 23.

It solves a puzzle about identifying groups of interconnected computers at a
LAN party. The puzzle involves finding sets of computers that are all directly
connected to each other (cliques) and locating the Chief Historian based on
computer naming patterns.

The solution uses graph theory to analyze network connections, finding both
small gaming groups (trios) that include specific computers and the largest
possible fully-connected group representing the actual LAN party location.

The module contains a Solution class that inherits from SolutionBase and
implements methods using rustworkx with custom clique detection.
"""

from itertools import combinations

import rustworkx as rx

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze computer networks and find LAN party groups using graph theory.

    This solution implements clique detection algorithms:
    - Part 1: Count trios of interconnected computers with Chief Historian hint
    - Part 2: Find the largest fully-connected group (maximum clique)

    The solution uses rustworkx graph library to model the network with manual
    clique finding implementation, which represent groups of computers that can
    all directly communicate with each other.
    """

    def construct_graph(self, data: list[str]) -> rx.PyGraph:
        """Construct an undirected graph from connection data.

        Creates a rustworkx graph where nodes represent computers and edges
        represent direct network connections between them. Each connection
        is bidirectional.

        Args:
            data (list[str]): List of connection strings in format "id1-id2"

        Returns
        -------
            rustworkx PyGraph object representing the computer network
        """
        graph = rx.PyGraph()
        node_map = {}

        for line in data:
            source, target = line.split("-")

            if source not in node_map:
                node_map[source] = graph.add_node(source)
            if target not in node_map:
                node_map[target] = graph.add_node(target)

            graph.add_edge(node_map[source], node_map[target], None)

        return graph

    def _bron_kerbosch_recursive(
        self, graph: rx.PyGraph, r: set[int], p: set[int], x: set[int], cliques: list[list[str]]
    ) -> None:
        """Recursive helper for Bron-Kerbosch algorithm.

        Args:
            graph: rustworkx PyGraph to search
            r: Current clique being built
            p: Candidate nodes to extend clique
            x: Already processed nodes
            cliques: List to accumulate found cliques
        """
        if not p and not x:
            cliques.append([graph[node] for node in r])
            return

        for v in list(p):
            neighbors = set(graph.neighbors(v))
            self._bron_kerbosch_recursive(graph, r | {v}, p & neighbors, x & neighbors, cliques)
            p.remove(v)
            x.add(v)

    def find_cliques(self, graph: rx.PyGraph) -> list[list[str]]:
        """Find all maximal cliques using Bron-Kerbosch algorithm.

        Args:
            graph: rustworkx PyGraph to search

        Returns
        -------
            List of maximal cliques, where each clique is a list of node labels
        """
        cliques: list[list[str]] = []
        all_nodes = set(graph.node_indices())
        self._bron_kerbosch_recursive(graph, set(), all_nodes, set(), cliques)
        return cliques

    def part1(self, data: list[str]) -> int:
        """Count sets of three interconnected computers including the Chief Historian.

        Finds all groups of three computers that are fully connected (each computer
        connected to the other two) and include at least one computer whose name
        starts with 't' (indicating the Chief Historian's potential location).

        Args:
            data (list[str]): List of connection strings representing the network

        Returns
        -------
            Number of unique trios containing at least one computer starting with 't'
        """
        graph = self.construct_graph(data)
        teacher_cliques = [
            clique
            for clique in self.find_cliques(graph)
            if len(clique) >= 3 and any(node.startswith("t") for node in clique)
        ]

        return len(
            {
                tuple(sorted(nodes))
                for clique in teacher_cliques
                for nodes in combinations(clique, 3)
                if any(node.startswith("t") for node in nodes)
            }
        )

    def part2(self, data: list[str]) -> str:
        """Find the password by identifying the largest LAN party group.

        Locates the maximum clique in the network graph, representing the largest
        set of computers where every computer is directly connected to every other
        computer. Returns the sorted computer names as a comma-separated password.

        Args:
            data (list[str]): List of connection strings representing the network

        Returns
        -------
            Password string of alphabetically sorted computer IDs joined by commas
        """
        graph = self.construct_graph(data)
        largest_clique = max(self.find_cliques(graph), key=len)
        return ",".join(sorted(largest_clique))
