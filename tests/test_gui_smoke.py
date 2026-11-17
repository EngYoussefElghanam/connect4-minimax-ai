"""GUI smoke tests: importable and expose the agreed API. Skipped when pygame is missing."""
import pytest

pytest.importorskip("pygame")


def test_modules_expose_expected_api():
    from connect4.ui.gui.app import run_gui
    from connect4.ui.gui.board_view import BoardView
    from connect4.ui.gui.menu_view import MenuView
    from connect4.ui.gui.tree_view import TreeView

    assert callable(run_gui)
    for cls, methods in [(BoardView, ["column_at", "draw", "animate_drop"]),
                         (MenuView, ["handle_event", "draw", "selected_k", "selected_heuristic"]),
                         (TreeView, ["set_tree", "handle_event", "draw"])]:
        for m in methods:
            assert hasattr(cls, m), f"{cls.__name__}.{m} missing"
