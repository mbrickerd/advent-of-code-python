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
implements methods using NetworkX to find cliques in the connection graph.
"""

from itertools import combinations

import networkx as nx

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze computer networks and find LAN party groups using graph theory.

    This solution implements clique detection algorithms:
    - Part 1: Count trios of interconnected computers with Chief Historian hint
    - Part 2: Find the largest fully-connected group (maximum clique)

    The solution uses NetworkX graph library to model the network and efficiently
    find all cliques, which represent groups of computers that can all directly
    communicate with each other.
    """

    def construct_graph(self, data: list[str]) -> nx.Graph:
        """Construct an undirected graph from connection data.

        Creates a NetworkX graph where nodes represent computers and edges
        represent direct network connections between them. Each connection
        is bidirectional.

        Args:
            data (list[str]): List of connection strings in format "id1-id2"

        Returns
        -------
            NetworkX Graph object representing the computer network
        """
        graph: nx.Graph = nx.Graph()
        edges = []
        for line in data:
            source, target = line.split("-")
            edges.append((source, target))
        graph.add_edges_from(edges)
        return graph

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
            for clique in nx.find_cliques(graph)
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
        largest_clique = max(nx.find_cliques(graph), key=len)
        return ",".join(sorted(largest_clique))
