"""Camera API Handler."""
import logging
import re

import viseron.webserver.api.v1.utils.response_generator as response_generator
from viseron.db.camera import get_camera, get_cameras
from viseron.webserver.api import BaseAPIHandler
from viseron.webserver.const import STATUS_ERROR_INTERNAL

LOGGER = logging.getLogger(__name__)


class CameraAPIHandler(BaseAPIHandler):
    """Handler for API calls related to config."""

    routes = [
        {
            "path_pattern": r"/camera/\d+",
            "supported_methods": ["GET"],
            "method": "get_camera",
        },
        {
            "path_pattern": r"/camera",
            "supported_methods": ["GET"],
            "method": "get_camera_definitions",
        },
    ]

    def get_camera_definitions(self, kwargs):
        """Return list of defined cameras."""
        fields = [["id"], ["name"]]

        fields_str = self.get_argument("fields", "")
        fields = (
            [x.split(".") for x in fields_str.split(",")]
            if fields_str and fields_str != "*"
            else fields
        )
        try:
            camera_definitions = get_cameras()

            if fields_str == "*":
                cameras = [x.__dict__ for x in camera_definitions]
            else:
                cameras = [
                    response_generator.get_resp_obj(x, fields)
                    for x in camera_definitions
                ]

            resp_obj = {"results": cameras}

            self.response_success(resp_obj)
            return
        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error(
                f"Error in API {self.__class__.__name__}.{kwargs['route']['method']}: "
                f"{str(error)}"
            )
            self.response_error(STATUS_ERROR_INTERNAL, reason=str(error))

    def get_camera(self, kwargs):
        """Get the information for one camera."""
        fields = [["id"], ["name"]]

        camera_id = int(re.search(r"/api/v1/camera/(\d+)", self.request.path).group(1))

        fields_str = self.get_argument("fields", "")
        fields = (
            [x.split(".") for x in fields_str.split(",")]
            if fields_str and fields_str != "*"
            else fields
        )
        try:
            camera = get_camera(camera_id)
            if fields_str == "*":
                resp_obj = camera.__dict__
            else:
                resp_obj = response_generator.get_resp_obj(camera, fields)

            self.response_success(resp_obj)
        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error(
                f"Error in API {self.__class__.__name__}.{kwargs['route']['method']}: "
                f"{str(error)}"
            )
            self.response_error(STATUS_ERROR_INTERNAL, reason=str(error))
