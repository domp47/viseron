"""Sqlite implementation of the database backend."""
import glob
import os
import pathlib
import sqlite3
from typing import List, Optional

from viseron.const import SQLITE_DB_PATH
from viseron.db import (
    AbstractCameraTable,
    AbstractMotionEventTable,
    AbstractRecordingTable,
    AbstractSqlUpdater,
    Camera,
)
from viseron.exceptions import DatabaseObjectNotFound

viseron_db_path = os.path.dirname(os.path.realpath(__file__))


class SqlUpdater(AbstractSqlUpdater):
    """Applies all database update patches to the SQLite database."""

    def __init__(self):
        super().__init__()
        # Get all sql schema files
        sql_files = glob.glob(os.path.join(viseron_db_path, "scripts", "*.sql"))
        sql_files.remove(os.path.join(viseron_db_path, "scripts", "init.sql"))
        sql_files.sort()

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='updates';"
            )
            results = cur.fetchall()

            # No DB Schema created so we need to run the init file.
            if not results:
                self.logger.info("DB file does not exist. Setting initial schema...")
                with open(
                    os.path.join(viseron_db_path, "scripts", "init.sql"), "r"
                ) as fp:
                    init_schema = fp.read()

                cur.executescript(init_schema)

            for sql_file in sql_files:
                update_name = pathlib.Path(sql_file).stem
                cur.execute(
                    "SELECT COUNT(*) FROM updates WHERE name = ?;", (update_name,)
                )
                result = cur.fetchone()
                if result == (0,):
                    self.logger.info(f"Applying DB Patch: {update_name}")
                    with open(sql_file, "r") as fp:
                        update = fp.read()

                    cur.executescript(update)

        self.logger.info("DB Up To Date")


class RecordingTable(AbstractRecordingTable):
    """Recording Table implementation in SQLite."""

    def remove(self, recording_id: int) -> None:
        """
        Remove recording from the database.

        Args:
            recording_id: id of the recording to remove
        """
        sql = """DELETE from recording
                 WHERE id = ?;"""

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM recording WHERE id = ?;", (recording_id,))
            res = cur.fetchone()
            if res == (0,):
                self.logger.error(
                    f"Cannot delete recording, No camera found with id: {recording_id}"
                )
                return

            cur.execute(sql, (recording_id,))

    def add_recording(self, recording) -> int:
        """
        Add a record to the Recording database table.

        Args:
            recording: Recording to add to the db

        Returns:
            int: The id of the row inserted
        """
        sql = "INSERT INTO recording (camera_id, time, filename) VALUES (?, ?, ?);"

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute(sql, (recording.camera_id, recording.time, recording.filename))

            return cur.lastrowid


class MotionEventTable(AbstractMotionEventTable):
    """Motion Event Table implementation in SQLite."""

    def add_motion_event(self, motion_event):
        """
        Add a record to the Motion Event database table.

        Args:
            motion_event: Motion Event to add to db

        Returns:
            int: The id of the row inserted
        """
        sql = "INSERT INTO motion_event (recording_id, timestamp_start, timestamp_end) VALUES (?, ?, ?);"

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute(
                sql,
                (
                    motion_event.recording_id,
                    motion_event.timestamp_start,
                    motion_event.timestamp_end,
                ),
            )

            return cur.lastrowid


class CameraTable(AbstractCameraTable):
    """Camera Table implementation in SQLite."""

    def get_all_cameras(self) -> List[Camera]:
        """
        Get all Camera definitions.

        Returns: List of Cameras
        """
        sql = """SELECT id, name, mqtt_name, stream_format_id, host, port, username, password, width, height, fps,
                  global_args, input_args, hwaccel_args, codec, audio_codec, rtsp_transport_id, filter_args,
                  frame_timeout, pix_fmt_id, substream_stream_format_id, substream_port, substream_path, substream_width,
                  substream_height, substream_fps, substream_input_args, substream_hwaccel_args, substream_codec,
                  substream_audio_codec, substream_rtsp_transport_id, substream_filter_args, substream_frame_timeout,
                  substream_pix_fmt_id, motion_interval, motion_trigger_detector, motion_trigger_recorder,
                  motion_timeout, motion_max_timeout, motion_width, motion_height, motion_frames, motion_log_level_id,
                  object_enabled, object_interval, object_labels, object_log_all_objects, object_max_frame_age,
                  object_log_level_id, publish_image, ffmpeg_log_level_id, ffmpeg_recoverable_errors,
                  ffprobe_log_level_id, log_level_id
                    FROM camera
                """

        cameras = []
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute(sql)
            while res := cur.fetchone():
                camera = Camera(
                    res[1],
                    res[2],
                    res[3],
                    res[4],
                    res[5],
                    res[6],
                    res[7],
                    res[8],
                    res[9],
                    res[10],
                    res[11],
                    res[12],
                    res[13],
                    res[14],
                    res[15],
                    res[16],
                    res[17],
                    res[18],
                    res[19],
                    res[20],
                    res[21],
                    res[22],
                    res[23],
                    res[24],
                    res[25],
                    res[26],
                    res[27],
                    res[28],
                    res[29],
                    res[30],
                    res[31],
                    res[32],
                    res[33],
                    res[34],
                    res[35],
                    res[36],
                    res[37],
                    res[38],
                    res[39],
                    res[40],
                    res[41],
                    res[42],
                    res[43],
                    res[44],
                    res[45],
                    res[46],
                    res[47],
                    res[48],
                    res[49],
                    res[50],
                    res[51],
                    res[52],
                    res[53],
                )
                camera.id = res[0]
                cameras.append(camera)

        return cameras

    @classmethod
    def __get_camera_by_key(cls, key: str, value: any) -> Optional[Camera]:
        """
        Get Camera definition by key and value.

        Args:
            key: to search for the camera.
            value: to search by for the camera

        Returns:
            Camera: Camera definition if found
            None: None if not found
        """
        sql = f"""SELECT id, name, mqtt_name, stream_format_id, host, port, username, password, width, height, fps,
                  global_args, input_args, hwaccel_args, codec, audio_codec, rtsp_transport_id, filter_args,
                  frame_timeout, pix_fmt_id, substream_stream_format_id, substream_port, substream_path, substream_width,
                  substream_height, substream_fps, substream_input_args, substream_hwaccel_args, substream_codec,
                  substream_audio_codec, substream_rtsp_transport_id, substream_filter_args, substream_frame_timeout,
                  substream_pix_fmt_id, motion_interval, motion_trigger_detector, motion_trigger_recorder,
                  motion_timeout, motion_max_timeout, motion_width, motion_height, motion_frames, motion_log_level_id,
                  object_enabled, object_interval, object_labels, object_log_all_objects, object_max_frame_age,
                  object_log_level_id, publish_image, ffmpeg_log_level_id, ffmpeg_recoverable_errors,
                  ffprobe_log_level_id, log_level_id
            FROM camera
            WHERE {key} = ?;"""

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute(sql, (value,))
            res = cur.fetchone()
            if not res:
                return None

            camera = Camera(
                res[1],
                res[2],
                res[3],
                res[4],
                res[5],
                res[6],
                res[7],
                res[8],
                res[9],
                res[10],
                res[11],
                res[12],
                res[13],
                res[14],
                res[15],
                res[16],
                res[17],
                res[18],
                res[19],
                res[20],
                res[21],
                res[22],
                res[23],
                res[24],
                res[25],
                res[26],
                res[27],
                res[28],
                res[29],
                res[30],
                res[31],
                res[32],
                res[33],
                res[34],
                res[35],
                res[36],
                res[37],
                res[38],
                res[39],
                res[40],
                res[41],
                res[42],
                res[43],
                res[44],
                res[45],
                res[46],
                res[47],
                res[48],
                res[49],
                res[50],
                res[51],
                res[52],
                res[53],
            )
            camera.id = res[0]

            return camera

    def get_camera_by_name(self, name: str) -> Optional[Camera]:
        """Get Camera definition by camera name."""
        return self.__get_camera_by_key("name", name)

    def get_camera_by_id(self, camera_id: int) -> Optional[Camera]:
        """Get Camera definition by camera id."""
        return self.__get_camera_by_key("id", camera_id)

    def add_camera(self, camera: Camera) -> int:
        """
        Create a camera.

        Args:
            camera: Camera definition to add to the db

        Returns:
            int: Id of created camera
        """
        sql = """INSERT INTO camera
                 (name, mqtt_name, stream_format_id, host, port, username, password, width, height, fps,
                  global_args, input_args, hwaccel_args, codec, audio_codec, rtsp_transport_id, filter_args,
                  frame_timeout, pix_fmt_id, substream_stream_format_id, substream_port, substream_path, substream_width,
                  substream_height, substream_fps, substream_input_args, substream_hwaccel_args, substream_codec,
                  substream_audio_codec, substream_rtsp_transport_id, substream_filter_args, substream_frame_timeout,
                  substream_pix_fmt_id, motion_interval, motion_trigger_detector, motion_trigger_recorder,
                  motion_timeout, motion_max_timeout, motion_width, motion_height, motion_frames, motion_log_level_id,
                  object_enabled, object_interval, object_labels, object_log_all_objects, object_max_frame_age,
                  object_log_level_id, publish_image, ffmpeg_log_level_id, ffmpeg_recoverable_errors,
                  ffprobe_log_level_id, log_level_id)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute(
                sql,
                (
                    camera.name,
                    camera.mqtt_name,
                    camera.stream_format_id,
                    camera.host,
                    camera.port,
                    camera.username,
                    camera.password,
                    camera.width,
                    camera.height,
                    camera.fps,
                    camera.global_args,
                    camera.input_args,
                    camera.hwaccel_args,
                    camera.codec,
                    camera.audio_codec,
                    camera.rtsp_transport_id,
                    camera.filter_args,
                    camera.frame_timeout,
                    camera.pix_fmt_id,
                    camera.substream_stream_format_id,
                    camera.substream_port,
                    camera.substream_path,
                    camera.substream_width,
                    camera.substream_height,
                    camera.substream_fps,
                    camera.substream_input_args,
                    camera.substream_hwaccel_args,
                    camera.substream_codec,
                    camera.substream_audio_codec,
                    camera.substream_rtsp_transport_id,
                    camera.substream_filter_args,
                    camera.substream_frame_timeout,
                    camera.substream_pix_fmt_id,
                    camera.motion_interval,
                    camera.motion_trigger_detector,
                    camera.motion_trigger_recorder,
                    camera.motion_timeout,
                    camera.motion_max_timeout,
                    camera.motion_width,
                    camera.motion_height,
                    camera.motion_frames,
                    camera.motion_log_level_id,
                    camera.object_enabled,
                    camera.object_interval,
                    camera.object_labels,
                    camera.object_log_all_objects,
                    camera.object_max_frame_age,
                    camera.object_log_level_id,
                    camera.publish_image,
                    camera.ffmpeg_log_level_id,
                    camera.ffmpeg_recoverable_errors,
                    camera.ffprobe_log_level_id,
                    camera.log_level_id,
                ),
            )

            return cur.lastrowid

    def update(self, camera: Camera) -> None:
        """
        Update an existing camera.

        Args:
            camera: Updated camera definition
        """
        sql = """UPDATE camera
                 SET
                   name = ?,
                   mqtt_name = ?,
                   stream_format_id = ?,
                   host = ?, port = ?,
                   username = ?,
                   password = ?,
                   width = ?,
                   height = ?,
                   fps = ?,
                   global_args = ?,
                   input_args = ?,
                   hwaccel_args = ?,
                   codec = ?,
                   audio_codec = ?,
                   rtsp_transport_id = ?,
                   filter_args = ?,
                   frame_timeout = ?,
                   pix_fmt_id = ?,
                   substream_stream_format_id = ?,
                   substream_port = ?,
                   substream_path = ?,
                   substream_width = ?,
                   substream_height = ?,
                   substream_fps = ?,
                   substream_input_args = ?,
                   substream_hwaccel_args = ?,
                   substream_codec = ?,
                   substream_audio_codec = ?,
                   substream_rtsp_transport_id = ?,
                   substream_filter_args = ?,
                   substream_frame_timeout = ?,
                   substream_pix_fmt_id = ?,
                   motion_interval = ?,
                   motion_trigger_detector = ?,
                   motion_trigger_recorder = ?,
                   motion_timeout = ?,
                   motion_max_timeout = ?,
                   motion_width = ?,
                   motion_height = ?,
                   motion_frames = ?,
                   motion_log_level_id = ?,
                   object_enabled = ?,
                   object_interval = ?,
                   object_labels = ?,
                   object_log_all_objects = ?,
                   object_max_frame_age = ?,
                   object_log_level_id = ?,
                   publish_image = ?,
                   ffmpeg_log_level_id = ?,
                   ffmpeg_recoverable_errors = ?,
                   ffprobe_log_level_id = ?,
                   log_level_id = ?
                 WHERE id = ?;"""
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM camera WHERE id = ?;", (camera.id,))
            res = cur.fetchone()
            if res == (0,):
                raise DatabaseObjectNotFound(
                    f"Cannot update camera, No camera found with id: {camera.id}"
                )

            cur.execute(
                sql,
                (
                    camera.name,
                    camera.mqtt_name,
                    camera.stream_format_id,
                    camera.host,
                    camera.port,
                    camera.username,
                    camera.password,
                    camera.width,
                    camera.height,
                    camera.fps,
                    camera.global_args,
                    camera.input_args,
                    camera.hwaccel_args,
                    camera.codec,
                    camera.audio_codec,
                    camera.rtsp_transport_id,
                    camera.filter_args,
                    camera.frame_timeout,
                    camera.pix_fmt_id,
                    camera.substream_stream_format_id,
                    camera.substream_port,
                    camera.substream_path,
                    camera.substream_width,
                    camera.substream_height,
                    camera.substream_fps,
                    camera.substream_input_args,
                    camera.substream_hwaccel_args,
                    camera.substream_codec,
                    camera.substream_audio_codec,
                    camera.substream_rtsp_transport_id,
                    camera.substream_filter_args,
                    camera.substream_frame_timeout,
                    camera.substream_pix_fmt_id,
                    camera.motion_interval,
                    camera.motion_trigger_detector,
                    camera.motion_trigger_recorder,
                    camera.motion_timeout,
                    camera.motion_max_timeout,
                    camera.motion_width,
                    camera.motion_height,
                    camera.motion_frames,
                    camera.motion_log_level_id,
                    camera.object_enabled,
                    camera.object_interval,
                    camera.object_labels,
                    camera.object_log_all_objects,
                    camera.object_max_frame_age,
                    camera.object_log_level_id,
                    camera.publish_image,
                    camera.ffmpeg_log_level_id,
                    camera.ffmpeg_recoverable_errors,
                    camera.ffprobe_log_level_id,
                    camera.log_level_id,
                    camera.id,
                ),
            )

    def delete(self, camera_id: int) -> None:
        """
        Delete a camera from the database.

        Args:
            camera_id: the id of the camera to delete
        """
        sql = """DELETE from camera
                 WHERE id = ?;"""

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM camera WHERE id = ?;", (camera_id,))
            res = cur.fetchone()
            if res == (0,):
                self.logger.error(
                    f"Cannot delete camera, No camera found with id: {camera_id}"
                )
                return

            cur.execute(sql, (camera_id,))
