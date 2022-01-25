"""Base for database backend."""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from viseron.config import ViseronConfig, load_config
from viseron.const import LOG_LEVELS
from viseron.db.models import Camera, MotionEvent, Recording
from viseron.helpers.logs import DuplicateFilter, ViseronLogFormat


class AbstractDatabaseBase(ABC):
    """Base class for all database classes."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = ViseronConfig(load_config())

        self.log_settings(self.config)

    def log_settings(self, _config):
        """Set custom log settings."""
        self.logger.propagate = False
        formatter = ViseronLogFormat(_config.logging)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.addFilter(DuplicateFilter())
        self.logger.addHandler(handler)

        self.logger.setLevel(LOG_LEVELS[_config.logging.level])
        logging.getLogger("apscheduler.scheduler").setLevel(logging.ERROR)
        logging.getLogger("apscheduler.executors").setLevel(logging.ERROR)


class AbstractSqlUpdater(AbstractDatabaseBase):
    """Class for running script updates. The class must update the database in the init method."""


class AbstractMotionEventTable(AbstractDatabaseBase):
    """Class for interfacing the motion event table."""

    @abstractmethod
    def add_motion_event(self, motion_event: MotionEvent) -> int:
        """
        Add a record to the Motion Event database table.

        Args:
            motion_event: Motion Event to add to db

        Returns:
            int: The id of the row inserted
        """


class AbstractRecordingTable(AbstractDatabaseBase):
    """Class for interfacing the recording table."""

    @abstractmethod
    def add_recording(self, recording: Recording) -> int:
        """
        Add a record to the Recording database table.

        Args:
            recording: Recording to add to the db

        Returns:
            int: The id of the row inserted
        """

    @abstractmethod
    def remove(self, recording_id: int) -> None:
        """
        Remove recording from the database.

        Args:
            recording_id: id of the recording to remove
        """


class AbstractCameraTable(AbstractDatabaseBase):
    """Class for interfacing the camera table."""

    @abstractmethod
    def add_camera(self, camera: Camera) -> int:
        """
        Create a camera.

        Args:
            camera: Camera definition to add to the db

        Returns:
            int: Id of created camera
        """

    @abstractmethod
    def get_all_cameras(self) -> List[Camera]:
        """
        Get all Camera definitions.

        Returns: List of Cameras
        """

    @abstractmethod
    def get_camera_by_name(self, name: str) -> Optional[Camera]:
        """
        Get Camera definition by camera name.

        Args:
            name: Name of the camera.

        Returns:
            Camera: Camera definition if found
            None: None if not found
        """

    @abstractmethod
    def get_camera_by_id(self, camera_id: int) -> Optional[Camera]:
        """
        Get Camera definition by camera id.

        Args:
            camera_id: id of the camera.

        Returns:
            Camera: Camera definition if found
            None: None if not found
        """

    @abstractmethod
    def update(self, camera: Camera) -> None:
        """
        Update an existing camera.

        Args:
            camera: Updated camera definition
        """

    @abstractmethod
    def delete(self, camera_id: int) -> None:
        """
        Delete a camera from the database.

        Args:
            camera_id: the id of the camera to delete
        """
