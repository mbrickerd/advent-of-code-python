from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    def get_differences(self, numbers: list[int]) -> list[list[int]]:
        rows = [numbers.copy()]

        while True:
            new_row = [b - a for a, b in zip(rows[-1], rows[-1][1:], strict=False)]

            # If all zeros, append an extra zero
            if all(x == 0 for x in new_row):
                new_row.append(0)
                rows.append(new_row)
                break

            rows.append(new_row)

        return rows

    def extrapolate(self, numbers: list[int], backwards: bool = False) -> int:
        rows = self.get_differences(numbers)

        if backwards:
            # Start from second to last row
            for i in range(len(rows) - 1, 0, -1):
                # Get the new first value by subtracting the first value of current row
                # from the first value of the row above it
                new_first = rows[i - 1][0] - rows[i][0]
                # Prepend this value to the row above
                rows[i - 1].insert(0, new_first)

            return rows[0][0]

        else:
            values = [row[-1] for row in rows[::-1]]
            return sum(values)

    def part1(self, data: list[str]) -> int:
        return sum([self.extrapolate(list(map(int, row.split()))) for row in data])

    def part2(self, data: list[str]) -> int:
        return sum([self.extrapolate(list(map(int, row.split())), backwards=True) for row in data])
