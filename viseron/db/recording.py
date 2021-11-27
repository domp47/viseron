"""Generic module to handle recordings for all database backends."""
import datetime

from viseron.db.loader import (
    get_camera_handler,
    get_motion_event_handler,
    get_recording_handler,
)
from viseron.db.models import MotionEvent, Recording
from viseron.exceptions import DatabaseObjectNotFound

recording_handler = get_recording_handler()
camera_handler = get_camera_handler()
motion_event_handler = get_motion_event_handler()


def __get_timestamp(delta: datetime.timedelta) -> str:
    """
    Convert a Time Delta into a human readable timestamp.

    Args:
        delta: Time Delta to convert to string

    Returns:
        str: String representation of the time delta
    """
    tot_sec = delta.seconds
    hours, remainder = divmod(tot_sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    ms, _ = divmod(delta.microseconds, 100)

    return "{:02}:{:02}:{:02}.{:04}".format(
        int(hours), int(minutes), int(seconds), int(ms)
    )


def add_recording(
    camera_name: str, segment_info: dict, event_start: int, filename: str
):
    """
    Add a recording and the motion events to the database.

    Args:
        camera_name: Name of the camera this recording belongs to
        segment_info: Dictionary of motion events
        event_start: The start time of the recording
        filename: The local filename of the recording
    """
    camera = camera_handler.get_camera_by_name(camera_name)

    if not camera:
        raise DatabaseObjectNotFound(f"Camera with {camera_name} not found.")

    recording_start = datetime.datetime.fromtimestamp(event_start)

    recording = Recording(camera.id, recording_start, filename)
    recording.id = recording_handler.add_recording(recording)

    for segment_file, event_info in segment_info.items():
        start_time = datetime.datetime.fromtimestamp(event_info["start_time"])
        end_time = datetime.datetime.fromtimestamp(event_info["end_time"])

        timestamp_start = start_time - recording_start
        timestamp_end = end_time - recording_start

        motion_event_handler.add_motion_event(
            MotionEvent(
                recording.id,
                __get_timestamp(timestamp_start),
                __get_timestamp(timestamp_end),
            )
        )
