"""Geometry helpers for circles and continuous 2D positions."""

from fork_royale.physics.vector import Vec2


def distance_squared(a: Vec2, b: Vec2) -> float:
    return (a - b).length_squared()


def circles_overlap(a_position: Vec2, a_radius: float, b_position: Vec2, b_radius: float) -> bool:
    combined = a_radius + b_radius
    return distance_squared(a_position, b_position) < combined * combined


def circle_intersection_depth(a_position: Vec2, a_radius: float, b_position: Vec2, b_radius: float) -> float:
    return a_radius + b_radius - a_position.distance_to(b_position)


def closest_point_on_segment(point: Vec2, start: Vec2, end: Vec2) -> Vec2:
    segment = end - start
    length_sq = segment.length_squared()
    if length_sq <= 1e-12:
        return start
    t = max(0.0, min(1.0, (point - start).dot(segment) / length_sq))
    return start + segment * t
