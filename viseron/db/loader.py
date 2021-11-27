"""Module to load the configured backend database module."""
import importlib

from viseron.config import load_config
from viseron.db import (
    AbstractCameraTable,
    AbstractMotionEventTable,
    AbstractRecordingTable,
    AbstractSqlUpdater,
)

config = load_config()
db_module = importlib.import_module(f"viseron.db.{config['database']['type']}")


def get_sql_updater() -> AbstractSqlUpdater:
    """Get the implemented Sql Updater."""
    return db_module.SqlUpdater()


def get_camera_handler() -> AbstractCameraTable:
    """Get the implemented Camera Handler."""
    return db_module.CameraTable()


def get_recording_handler() -> AbstractRecordingTable:
    """Get the implemented Recording Handler."""
    return db_module.RecordingTable()


def get_motion_event_handler() -> AbstractMotionEventTable:
    """Get the implemented Motion Event Handler."""
    return db_module.MotionEventTable()
