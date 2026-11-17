from connect4 import config
from connect4.board import Board
from connect4.ai.tree import TreeNode
from connect4.ui.console.renderer import render_board, render_scores, render_stats
from connect4.ui.console.tree_printer import format_node, format_tree, write_tree_to_file
import sample_boards as sb


# ---------------------------------------------------------------- board / scores
def test_render_board_has_a_line_per_row_plus_column_footer(empty_board):
    lines = render_board(empty_board).splitlines()
    assert len(lines) >= config.ROWS + 1
    footer = lines[-1]
    assert all(str(c) in footer for c in range(1, config.COLS + 1))


def test_render_board_distinguishes_players():
    human = render_board(Board.from_strings(sb.H_EDGE))
    ai = render_board(Board.from_strings(sb.A_EDGE))
    empty = render_board(Board())
    assert len({human, ai, empty}) == 3


def test_render_scores_contains_both_scores():
    out = render_scores(3, 5)
    assert "3" in out and "5" in out


def test_render_stats_contains_numbers():
    out = render_stats(nodes_expanded=1234, elapsed_seconds=0.5, prunes=77)
    assert "1234" in out and "77" in out


# ---------------------------------------------------------------- tree printer
def small_tree():
    leaf = TreeNode(depth=2, is_max=True, move=1, value=7.5, is_leaf=True)
    pruned = TreeNode(depth=2, is_max=True, move=2, pruned=True)
    a = TreeNode(depth=1, is_max=False, move=0, value=3, children=[leaf, pruned])
    b = TreeNode(depth=1, is_max=False, move=4, value=3)
    return TreeNode(depth=0, is_max=True, move=None, value=3, children=[a, b])


def test_one_line_per_node():
    assert len(format_tree(small_tree()).splitlines()) == 5


def test_shows_max_min_labels():
    out = format_tree(small_tree())
    assert "MAX" in out and "MIN" in out


def test_children_are_indented_deeper_than_parent():
    lines = format_tree(small_tree()).splitlines()
    indent = [len(l) - len(l.lstrip()) for l in lines]
    assert indent[0] < indent[1] < indent[2]


def test_columns_are_shown_one_based():
    lines = format_tree(small_tree()).splitlines()
    assert "col=1" in lines[1]          # move 0
    assert "col=2" in lines[2]          # move 1 (the leaf)


def test_leaf_value_and_pruned_marker():
    lines = format_tree(small_tree()).splitlines()
    assert "7.5" in lines[2]
    assert "PRUNED" in lines[3] and "col=3" in lines[3]
    assert sum("PRUNED" in l for l in lines) == 1


def test_max_depth_truncates_output():
    assert len(format_tree(small_tree(), max_depth=1).splitlines()) == 3


def test_format_node_is_a_single_line():
    assert "\n" not in format_node(small_tree().children[0])


def test_show_boards_adds_board_drawing_for_leaves():
    leaf = TreeNode(depth=1, is_max=False, move=3, value=2.0, is_leaf=True,
                    board=Board.from_strings(sb.MID_GAME))
    root = TreeNode(depth=0, is_max=True, move=None, value=2.0, children=[leaf])
    assert len(format_tree(root, show_boards=True).splitlines()) > len(format_tree(root).splitlines())


def test_write_tree_to_file(tmp_path):
    root = small_tree()
    target = tmp_path / "tree.txt"
    write_tree_to_file(root, str(target))
    assert target.read_text().strip() == format_tree(root).strip()
