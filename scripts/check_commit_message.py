import re
import sys
from pathlib import Path

PATTERN = re.compile(
    r"^(feat|fix|improve|test)"
    r"(\([a-z0-9-]+\))?"
    r"(!)?: .+"
)


def main() -> int:
    message_file = Path(sys.argv[1])
    message = message_file.read_text(encoding="utf-8").splitlines()[0]

    if PATTERN.fullmatch(message):
        return 0

    print(f"Invalid commit message: {message}")
    print("Expected: type(scope): description")
    print("Example: feat(orders): add order confirmation")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())