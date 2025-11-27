"""
Utility for managing Advent of Code authentication credentials.

Provides methods to retrieve project paths and authentication details
for interacting with the Advent of Code platform.
"""

import os
from pathlib import Path


class Authenticator:
    """Utility class for retrieving Advent of Code authentication details."""

    @staticmethod
    def get_path() -> Path:
        """
        Determine the absolute path to the project directory.

        Returns
        -------
            Path to the directory containing the current script or script's parent.
        """
        current_file = Path(__file__).resolve()
        aoc_dir = current_file.parent.parent
        return aoc_dir.parent

    @staticmethod
    def get_headers() -> dict[str, str]:
        """
        Construct HTTP headers for Advent of Code API requests.

        Returns
        -------
            Dictionary of HTTP headers for API requests.

        Raises
        ------
            ValueError: If AOC_SESSION, GITHUB_USERNAME, or GITHUB_USER_EMAIL environment
                variables are not set.
        """
        session = os.getenv("AOC_SESSION")
        username = os.getenv("GITHUB_USERNAME")
        email = os.getenv("GITHUB_USER_EMAIL")

        if not username or not email:
            err_msg = "GITHUB_USERNAME and GITHUB_USER_EMAIL environment variables are not set"
            raise ValueError(err_msg)

        return {"Cookie": f"session={session}", "User-Agent": f"{username} (contact: {email})"}
