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


def test_keyboard_k_and_gui_terminal_tree(monkeypatch, capsys):
    import pygame
    from connect4.ui.gui.app import _GuiApp
    monkeypatch.setenv('SDL_VIDEODRIVER', 'dummy')
    monkeypatch.setenv('SDL_AUDIODRIVER', 'dummy')
    app = _GuiApp(None, None, True)
    try:
        menu = app.menu
        menu.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=menu._k_field.center))
        for digit in '1000':
            menu.handle_event(pygame.event.Event(pygame.KEYDOWN, key=ord(digit), unicode=digit, mod=0))
        assert menu.selected_k() == 1000
        menu.draw(app.screen)
        menu.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=menu._k_field.center))
        menu.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode='', mod=0))
        assert not menu.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=menu._start.rect.center))
        app.start_game(2, 'composite')
        monkeypatch.setattr(app.board_view, 'animate_drop', lambda *args: None)
        app._human_click((80, 200))
        app._ai_turn()
        app._draw_frame(app.game.board)
        assert app.tree_view.root is not None
        out = capsys.readouterr().out
        assert '[MAX] root' in out and 'leaf' in out and 'score_diff:' in out
        assert '1 2 3 4 5 6 7' in out
    finally:
        pygame.quit()
