import re

def to_snake_case(name: str) -> str:
    name = name.strip()
    name = name.lower()

    # Replace spaces, dashes, and slashes with underscores
    name = re.sub(r"[ \-\/]+", "_", name)

    # Remove all other non-word characters except underscores
    name = re.sub(r"[^\w_]", "", name)

    # Collapse multiple underscores
    name = re.sub(r"_+", "_", name)

    # Strip leading/trailing underscores
    return name.strip("_")
