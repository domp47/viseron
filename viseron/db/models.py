"""Models to represent that database tables."""
from datetime import datetime


class Camera:
    """Object that represents that camera table."""

    def __init__(
        self,
        name: str,
        mqtt_name: str,
        stream_format_id: int,
        host: str,
        port: int,
        username: str,
        password: str,
        width: int,
        height: int,
        fps: int,
        global_args: str,
        input_args: str,
        hwaccel_args: str,
        codec: str,
        audio_codec: str,
        rtsp_transport_id: int,
        filter_args: str,
        frame_timeout: str,
        pix_fmt_id: int,
        substream_stream_format_id: int,
        substream_port: int,
        substream_path: str,
        substream_width: int,
        substream_height: int,
        substream_fps: str,
        substream_input_args: str,
        substream_hwaccel_args: str,
        substream_codec: str,
        substream_audio_codec: str,
        substream_rtsp_transport_id: int,
        substream_filter_args: str,
        substream_frame_timeout: int,
        substream_pix_fmt_id: int,
        motion_interval: float,
        motion_trigger_detector: bool,
        motion_trigger_recorder: bool,
        motion_timeout: bool,
        motion_max_timeout: int,
        motion_width: int,
        motion_height: int,
        motion_frames: int,
        motion_log_level_id: int,
        object_enabled: bool,
        object_interval: int,
        object_labels: str,
        object_log_all_objects: bool,
        object_max_frame_age: float,
        object_log_level_id: int,
        publish_image: bool,
        ffmpeg_log_level_id: int,
        ffmpeg_recoverable_errors: str,
        ffprobe_log_level_id: int,
        log_level_id: int,
    ):
        self.id = None
        self.name = name
        self.mqtt_name = mqtt_name
        self.stream_format_id = stream_format_id
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.width = width
        self.height = height
        self.fps = fps
        self.global_args = global_args
        self.input_args = input_args
        self.hwaccel_args = hwaccel_args
        self.codec = codec
        self.audio_codec = audio_codec
        self.rtsp_transport_id = rtsp_transport_id
        self.filter_args = filter_args
        self.frame_timeout = frame_timeout
        self.pix_fmt_id = pix_fmt_id
        self.substream_stream_format_id = substream_stream_format_id
        self.substream_port = substream_port
        self.substream_path = substream_path
        self.substream_width = substream_width
        self.substream_height = substream_height
        self.substream_fps = substream_fps
        self.substream_input_args = substream_input_args
        self.substream_hwaccel_args = substream_hwaccel_args
        self.substream_codec = substream_codec
        self.substream_audio_codec = substream_audio_codec
        self.substream_rtsp_transport_id = substream_rtsp_transport_id
        self.substream_filter_args = substream_filter_args
        self.substream_frame_timeout = substream_frame_timeout
        self.substream_pix_fmt_id = substream_pix_fmt_id
        self.motion_interval = motion_interval
        self.motion_trigger_detector = motion_trigger_detector
        self.motion_trigger_recorder = motion_trigger_recorder
        self.motion_timeout = motion_timeout
        self.motion_max_timeout = motion_max_timeout
        self.motion_width = motion_width
        self.motion_height = motion_height
        self.motion_frames = motion_frames
        self.motion_log_level_id = motion_log_level_id
        self.object_enabled = object_enabled
        self.object_interval = object_interval
        self.object_labels = object_labels
        self.object_log_all_objects = object_log_all_objects
        self.object_max_frame_age = object_max_frame_age
        self.object_log_level_id = object_log_level_id
        self.publish_image = publish_image
        self.ffmpeg_log_level_id = ffmpeg_log_level_id
        self.ffmpeg_recoverable_errors = ffmpeg_recoverable_errors
        self.ffprobe_log_level_id = ffprobe_log_level_id
        self.log_level_id = log_level_id


class MotionEvent:
    """Object that represents that motin event table."""

    def __init__(self, recording_id: int, timestamp_start: str, timestamp_end: str):
        self.id = None
        self.recording_id = recording_id
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end


class Recording:
    """Object that represents that recording table."""

    def __init__(self, camera_id: int, time: datetime, filename: str):
        self.id = None
        self.camera_id = camera_id
        self.time = time
        self.filename = filename
