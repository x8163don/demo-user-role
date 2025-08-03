import dataclasses


def dedupe(items: list[int]) -> list[int]:
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]


@dataclasses
class RegionInput:
    region: str = "HQ"
