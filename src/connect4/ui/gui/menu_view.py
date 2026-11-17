"""Start screen: difficulty buttons (Easy/Medium/Hard) + custom K input + heuristic picker."""
from __future__ import annotations


class MenuView:
    def __init__(self, screen) -> None:
        # TODO
        raise NotImplementedError

    def handle_event(self, event) -> None:
        """Update hover / selection / text-box state."""
        # TODO
        raise NotImplementedError

    def draw(self) -> None:
        # TODO
        raise NotImplementedError

    def selected_k(self) -> int | None:
        """K chosen via difficulty button or valid custom input, else None."""
        # TODO
        raise NotImplementedError

    def selected_heuristic(self) -> str:
        # TODO
        raise NotImplementedError
