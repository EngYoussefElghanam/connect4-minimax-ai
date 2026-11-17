import pytest

from connect4.board import Board
from connect4.ai.heuristics.composite import CompositeHeuristic
from connect4.ai.heuristics.score_diff import ScoreDifferenceHeuristic
from connect4.ai.minimax import MinimaxAgent
from connect4.ai.tree import TreeNode, count_nodes, iter_nodes, tree_depth
import sample_boards as sb


def run(board, k, **kw):
    return MinimaxAgent(ScoreDifferenceHeuristic(), k, **kw).choose_move(board)


# ---------------------------------------------------------------- tree utilities
def _small_tree():
    leaf = TreeNode(depth=2, is_max=True, move=1, value=7.5, is_leaf=True)
    pruned = TreeNode(depth=2, is_max=True, move=2, pruned=True)
    a = TreeNode(depth=1, is_max=False, move=0, value=3, children=[leaf, pruned])
    b = TreeNode(depth=1, is_max=False, move=4, value=3)
    return TreeNode(depth=0, is_max=True, move=None, value=3, children=[a, b])


def test_iter_nodes_visits_everything_preorder():
    root = _small_tree()
    nodes = list(iter_nodes(root))
    assert len(nodes) == 5 and nodes[0] is root


def test_count_nodes_with_and_without_pruned():
    root = _small_tree()
    assert count_nodes(root) == 5
    assert count_nodes(root, include_pruned=False) == 4


def test_tree_depth():
    assert tree_depth(_small_tree()) == 2
    assert tree_depth(TreeNode(depth=0, is_max=True, move=None)) == 0


# ---------------------------------------------------------------- tree produced by the agent
def test_no_tree_when_recording_disabled(mid_game_board):
    assert run(mid_game_board, 2, record_tree=False).tree is None


def test_unpruned_tree_shape_on_empty_board(empty_board):
    r = run(empty_board, 2, use_pruning=False)
    assert count_nodes(r.tree) == 1 + 7 + 49
    assert r.stats.nodes_expanded == 57
    assert r.tree.is_max and r.tree.depth == 0 and r.tree.move is None
    assert all(not c.is_max and c.depth == 1 for c in r.tree.children)


def test_tree_depth_equals_k(mid_game_board):
    for k in (1, 2, 3):
        assert tree_depth(run(mid_game_board, k).tree) == k


def test_leaves_have_values_and_boards(mid_game_board):
    r = run(mid_game_board, 2, use_pruning=False)
    leaves = [n for n in iter_nodes(r.tree) if n.is_leaf]
    assert leaves and all(n.value is not None and n.board is not None for n in leaves)
    assert all(n.depth == 2 for n in leaves)


def test_leaves_carry_heuristic_breakdown(mid_game_board):
    r = MinimaxAgent(CompositeHeuristic(), 2, use_pruning=False).choose_move(mid_game_board)
    leaves = [n for n in iter_nodes(r.tree) if n.is_leaf]
    assert all(n.heuristic_breakdown for n in leaves)


def test_root_value_matches_result(mid_game_board):
    r = run(mid_game_board, 3)
    assert r.tree.value == pytest.approx(r.value)


def test_internal_values_are_max_or_min_of_children_without_pruning(mid_game_board):
    r = run(mid_game_board, 3, use_pruning=False)
    for n in iter_nodes(r.tree):
        if n.children:
            vals = [c.value for c in n.children]
            assert n.value == pytest.approx(max(vals) if n.is_max else min(vals))


def test_max_min_levels_alternate(mid_game_board):
    r = run(mid_game_board, 3)
    for n in iter_nodes(r.tree):
        assert n.is_max == (n.depth % 2 == 0)


def test_children_moves_are_legal_columns(mid_game_board):
    r = run(mid_game_board, 2, use_pruning=False)
    assert sorted(c.move for c in r.tree.children) == mid_game_board.valid_moves()


def test_pruned_nodes_are_marked_and_not_counted_as_expanded(mid_game_board):
    r = run(mid_game_board, 4, use_pruning=True)
    pruned = [n for n in iter_nodes(r.tree) if n.pruned]
    assert pruned
    assert all(not n.children and n.value is None for n in pruned)
    assert count_nodes(r.tree, include_pruned=False) == r.stats.nodes_expanded
