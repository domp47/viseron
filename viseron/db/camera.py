"""Generic module to handle cameras for all database backends."""

from viseron.db.loader import get_camera_handler

camera_handler = get_camera_handler()


def get_cameras():
    """Get all Cameras in the database."""
    return camera_handler.get_all_cameras()


def get_camera(camera_id: int):
    """Get camera in database by id."""
    return camera_handler.get_camera_by_id(camera_id)
