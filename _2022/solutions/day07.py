"""Day 7: No Space Left On Device

This module provides the solution for Advent of Code 2022 - Day 7.
It handles parsing filesystem terminal output to build a directory tree
and calculating directory sizes to identify candidates for deletion.

The module contains a Solution class that inherits from SolutionBase and implements
methods to construct a filesystem graph and calculate space requirements.
"""

import rustworkx as rx

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Analyze filesystem directory sizes for space management.

    This solution processes terminal output from ls and cd commands to construct
    a filesystem tree. Part 1 finds directories under 100000 bytes in size, while
    Part 2 identifies the smallest directory that can be deleted to free enough
    space for a system update.

    The solution uses a directed graph to represent the filesystem hierarchy and
    topological sorting to efficiently calculate directory sizes bottom-up.
    """

    def get_current_dir(self, current_path: list[str]) -> str:
        """Construct full directory path from path components.

        Args:
            current_path: List of directory names from root to current location

        Returns
        -------
            str: Full path string with components joined by forward slashes
        """
        return "/".join(current_path) if len(current_path) > 1 else "/"

    def construct_graph(self, data: list[str]) -> rx.PyDiGraph:
        """Parse terminal output into filesystem directory graph.

        Processes cd and ls commands to build a directed graph representing
        the filesystem structure, with nodes for directories and files.

        Args:
            data: List of terminal output lines containing commands and file listings

        Returns
        -------
            rx.PyDiGraph: Directed graph where nodes represent directories/files
                with metadata (name, type, size) and edges represent parent-child
                relationships
        """
        graph = rx.PyDiGraph()

        # Add root node
        root = graph.add_node({"name": "/", "type": "dir", "size": None})

        # Dictionary to track current path and node indices
        node_map = {"/": root}
        current_path = ["/"]
        current_node = root

        for line in data:
            if line.startswith("$ cd"):
                dir_name = line.split()[-1]

                if dir_name == "/":
                    current_path = ["/"]
                    current_node = root

                elif dir_name == "..":
                    current_path.pop()
                    current_node = node_map[self.get_current_dir(current_path)]

                else:
                    current_path.append(dir_name)
                    current_node = node_map[self.get_current_dir(current_path)]

            elif line.startswith("$ ls"):
                continue

            elif line.startswith("dir"):
                dir_name = line.split()[1]
                full_path = self.get_current_dir(current_path) + "/" + dir_name
                new_node = graph.add_node({"name": dir_name, "type": "dir", "size": None})
                graph.add_edge(current_node, new_node, None)
                node_map[full_path] = new_node

            elif line.strip():  # File entry
                size, filename = line.split()
                file_node = graph.add_node({"name": filename, "type": "file", "size": int(size)})
                graph.add_edge(current_node, file_node, None)

        return graph

    def calculate_directory_sizes(self, graph: rx.PyDiGraph) -> dict[int, int]:
        """Calculate total size of each directory including nested contents.

        Uses topological sorting to process directories bottom-up, ensuring
        child sizes are calculated before parent directories.

        Args:
            graph: Directed graph representing filesystem structure

        Returns
        -------
            dict[int, int]: Mapping of node indices to their total sizes,
                where directory sizes include all nested files and subdirectories
        """
        sizes: dict[int, int] = {}

        # Process nodes bottom-up (children before parents)
        for node_idx in reversed(rx.topological_sort(graph)):
            node_data = graph[node_idx]

            if node_data["type"] == "file":
                sizes[node_idx] = node_data["size"]
            else:
                # Directory: sum all children using out_edges to get child indices
                child_indices = [edge[1] for edge in graph.out_edges(node_idx)]
                sizes[node_idx] = sum(sizes[child] for child in child_indices)

        return sizes

    def part1(self, data: list[str]) -> int:
        """Find sum of directory sizes that are at most 100000 bytes.

        Identifies all directories with total size ≤ 100000 bytes (including
        nested contents) and returns their sum for cleanup analysis.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Sum of total sizes for all directories with size ≤ 100000
        """
        graph = self.construct_graph(data)
        sizes = self.calculate_directory_sizes(graph)

        return sum(
            size for idx, size in sizes.items() if graph[idx]["type"] == "dir" and size <= 100000
        )

    def part2(self, data: list[str]) -> int:
        """Find smallest directory to delete for system update space.

        Calculates minimum space needed for update (30000000 total required)
        and identifies the smallest directory that would free enough space.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Size of the smallest directory that, if deleted, would free
                enough space for the 30000000 byte system update
        """
        graph = self.construct_graph(data)
        sizes = self.calculate_directory_sizes(graph)

        total_space = 70000000
        update_space = 30000000
        root_size = sizes[0]

        current_free = total_space - root_size
        min_to_free = update_space - current_free

        return min(
            size
            for idx, size in sizes.items()
            if graph[idx]["type"] == "dir" and size >= min_to_free
        )
