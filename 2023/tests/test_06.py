from aoc.models.tester import TestSolutionUtility


def test_day06_part1():
    TestSolutionUtility.run_test(
        year=2023,
        day=6,
        is_raw=False,
        part_num=1,
        expected=288,
    )


def test_day06_part2():
    TestSolutionUtility.run_test(
        year=2023,
        day=6,
        is_raw=False,
        part_num=2,
        expected=71503,
    )
