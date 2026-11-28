import argparse
import sys
from typing import List


def parse_numbers(args: List[str]) -> List[float]:
    numbers = []
    for arg in args:
        try:
            numbers.append(float(arg))
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid number: {arg}")
    return numbers


def compute_statistics(numbers: List[float]) -> dict:
    if not numbers:
        raise ValueError("No numbers provided for statistics.")
    total = sum(numbers)
    count = len(numbers)
    return {
        "count": count,
        "sum": total,
        "average": total / count,
        "min": min(numbers),
        "max": max(numbers),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute basic statistics (sum, average, min, max) for a list of numbers."
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        help="Numbers to process (integers or floats).",
    )
    args = parser.parse_args()
    try:
        numbers = parse_numbers(args.numbers)
        stats = compute_statistics(numbers)
        print(f"Count:   {stats['count']}")
        print(f"Sum:     {stats['sum']}")
        print(f"Average: {stats['average']}")
        print(f"Min:     {stats['min']}")
        print(f"Max:     {stats['max']}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()