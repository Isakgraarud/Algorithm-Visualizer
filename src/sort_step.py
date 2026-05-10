from dataclasses import dataclass, field


@dataclass
class SortStep:
    data: list
    color_map: dict  = field(default_factory=dict)   # {index: role_str}
    sorted_set: set  = field(default_factory=set)    # indices that are permanently sorted
    variables: dict  = field(default_factory=dict)   # {'i': 0, 'j': 3, 'pivot': 42}
    pseudocode_line: int = -1
    log: str = ""
    comparisons_delta: int = 0
    swaps_delta: int = 0
