"""Small reusable drawing helpers for the playful pygame GUI."""
from __future__ import annotations

from math import cos, pi, sin

import pygame

from connect4.ui.gui import theme


Color = tuple[int, int, int]


def _mix(a: Color, b: Color, t: float) -> Color:
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def brighten(color: Color, amount: float) -> Color:
    return _mix(color, (255, 255, 255), amount)


def darken(color: Color, amount: float) -> Color:
    return _mix(color, (0, 0, 0), amount)


def draw_vertical_gradient(surface: pygame.Surface, rect: pygame.Rect | tuple[int, int, int, int],
                           top: Color, bottom: Color) -> None:
    rect = pygame.Rect(rect)
    if rect.height <= 0:
        return
    for i in range(rect.height):
        t = i / max(1, rect.height - 1)
        pygame.draw.line(surface, _mix(top, bottom, t),
                         (rect.x, rect.y + i), (rect.right - 1, rect.y + i))


def draw_panel(surface: pygame.Surface, rect: pygame.Rect | tuple[int, int, int, int],
               fill: Color, border: Color | None = None, *, radius: int = 20,
               shadow_offset: tuple[int, int] = (0, 6), shadow_alpha: int = 70) -> pygame.Rect:
    rect = pygame.Rect(rect)
    shadow = pygame.Surface((rect.width + abs(shadow_offset[0]) + 8,
                             rect.height + abs(shadow_offset[1]) + 8), pygame.SRCALPHA)
    shadow_rect = pygame.Rect(4 + max(shadow_offset[0], 0), 4 + max(shadow_offset[1], 0),
                              rect.width, rect.height)
    pygame.draw.rect(shadow, (0, 0, 0, shadow_alpha), shadow_rect, border_radius=radius)
    surface.blit(shadow, (rect.x - 4 - min(shadow_offset[0], 0), rect.y - 4 - min(shadow_offset[1], 0)))
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, border or brighten(fill, 0.22), rect, width=2, border_radius=radius)
    return rect


def draw_star(surface: pygame.Surface, center: tuple[int, int], radius: int,
              color: Color, inner_ratio: float = 0.45) -> None:
    cx, cy = center
    points = []
    for i in range(10):
        angle = -pi / 2 + i * pi / 5
        r = radius if i % 2 == 0 else radius * inner_ratio
        points.append((cx + cos(angle) * r, cy + sin(angle) * r))
    pygame.draw.polygon(surface, color, points)


def draw_cloud(surface: pygame.Surface, pos: tuple[int, int], scale: float = 1.0) -> None:
    x, y = pos
    colour = theme.CLOUD
    outline = theme.CLOUD_OUTLINE
    circles = [
        (x, y + 6 * scale, 16 * scale),
        (x + 18 * scale, y, 20 * scale),
        (x + 42 * scale, y + 4 * scale, 18 * scale),
        (x + 60 * scale, y + 10 * scale, 14 * scale),
    ]
    for cx, cy, r in circles:
        pygame.draw.circle(surface, colour, (int(cx), int(cy)), int(r))
        pygame.draw.circle(surface, outline, (int(cx), int(cy)), int(r), 2)
    base = pygame.Rect(int(x - 8 * scale), int(y + 10 * scale), int(80 * scale), int(24 * scale))
    pygame.draw.rect(surface, colour, base, border_radius=int(12 * scale))
    pygame.draw.rect(surface, outline, base, width=2, border_radius=int(12 * scale))


def draw_smiley_disc(surface: pygame.Surface, center: tuple[int, int], radius: int,
                     color: Color, *, outline: Color | None = None,
                     mood: str = "happy", accessory: str | None = None) -> None:
    outline = outline or darken(color, 0.35)
    pygame.draw.circle(surface, color, center, radius)
    pygame.draw.circle(surface, outline, center, radius, 3)
    highlight = (center[0] - radius // 3, center[1] - radius // 3)
    pygame.draw.circle(surface, brighten(color, 0.35), highlight, max(4, radius // 4))

    eye_y = center[1] - radius // 5
    eye_dx = radius // 3
    eye_r = max(2, radius // 10)
    for sign in (-1, 1):
        eye = (center[0] + sign * eye_dx, eye_y)
        if mood == "wink" and sign == 1:
            pygame.draw.line(surface, outline, (eye[0] - eye_r, eye[1]), (eye[0] + eye_r, eye[1]), 3)
        else:
            pygame.draw.circle(surface, outline, eye, eye_r)
    mouth_rect = pygame.Rect(center[0] - radius // 3, center[1] - radius // 10,
                             2 * radius // 3, 2 * radius // 3)
    if mood == "surprised":
        pygame.draw.circle(surface, outline, (center[0], center[1] + radius // 5), max(3, radius // 8), 3)
    else:
        start, end = (1.15 * pi, 1.85 * pi) if mood != "sad" else (0.15 * pi, 0.85 * pi)
        pygame.draw.arc(surface, outline, mouth_rect, start, end, 3)

    if accessory == "cap":
        brim = pygame.Rect(center[0] - radius // 2, center[1] - radius + 2, radius, radius // 4)
        top = [(center[0] - radius // 3, center[1] - radius + 4),
               (center[0] + radius // 3, center[1] - radius + 4),
               (center[0] + radius // 6, center[1] - radius - radius // 3),
               (center[0] - radius // 2, center[1] - radius - radius // 6)]
        pygame.draw.polygon(surface, theme.CAP_BLUE, top)
        pygame.draw.rect(surface, theme.CAP_BLUE, brim, border_radius=4)
        pygame.draw.rect(surface, darken(theme.CAP_BLUE, 0.25), brim, width=2, border_radius=4)
    elif accessory == "bow":
        left = [(center[0] - radius // 2, center[1] - radius + 8),
                (center[0] - radius // 6, center[1] - radius // 2),
                (center[0] - radius // 8, center[1] - radius + 4)]
        right = [(center[0] + radius // 2, center[1] - radius + 8),
                 (center[0] + radius // 6, center[1] - radius // 2),
                 (center[0] + radius // 8, center[1] - radius + 4)]
        pygame.draw.polygon(surface, theme.BOW_PINK, left)
        pygame.draw.polygon(surface, theme.BOW_PINK, right)
        pygame.draw.circle(surface, brighten(theme.BOW_PINK, 0.2),
                           (center[0], center[1] - radius + 6), max(4, radius // 8))


def draw_speech_bubble(surface: pygame.Surface, rect: pygame.Rect | tuple[int, int, int, int],
                       fill: Color, text_color: Color, font: pygame.font.Font,
                       text: str, tail_to: tuple[int, int] | None = None) -> pygame.Rect:
    rect = pygame.Rect(rect)
    draw_panel(surface, rect, fill, brighten(fill, 0.2), radius=18, shadow_alpha=55)
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if font.size(trial)[0] <= rect.width - 22:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = rect.y + 10
    for line in lines[:3]:
        img = font.render(line, True, text_color)
        surface.blit(img, (rect.x + 11, y))
        y += img.get_height() + 2
    if tail_to is not None:
        tail = [(rect.x + 28, rect.bottom - 2), (rect.x + 58, rect.bottom - 2), tail_to]
        pygame.draw.polygon(surface, fill, tail)
        pygame.draw.lines(surface, brighten(fill, 0.2), False, tail + [tail[0]], 2)
    return rect


def draw_dashed_line(surface: pygame.Surface, color: Color, start: tuple[float, float],
                     end: tuple[float, float], *, width: int = 2,
                     dash: int = 8, gap: int = 5) -> None:
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    dist = max(1.0, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / dist, dy / dist
    pos = 0.0
    while pos < dist:
        a = pos
        b = min(pos + dash, dist)
        seg_start = (x1 + ux * a, y1 + uy * a)
        seg_end = (x1 + ux * b, y1 + uy * b)
        pygame.draw.line(surface, color, seg_start, seg_end, width)
        pos += dash + gap
