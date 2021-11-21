"""Camera API Handler."""
import logging

from viseron.nvr import FFMPEGNVR
from viseron.webserver.api import BaseAPIHandler
from viseron.webserver.const import STATUS_ERROR_INTERNAL
import viseron.webserver.api.v1.utils.response_generator as response_generator

LOGGER = logging.getLogger(__name__)


class CameraAPIHandler(BaseAPIHandler):
    """Handler for API calls related to config."""

    routes = [
        {
            "path_pattern": r"/camera",
            "supported_methods": ["GET"],
            "method": "get_camera_definitions",
        },
    ]

    def get_camera_definitions(self, kwargs):
        """Return list of defined cameras"""
        fields = [["camera", "stream", "width"], ["camera", "stream", "height"], ["config", "camera", "name"],
                  ["config", "camera", "name_slug"], ["config", "camera", "host"]]

        try:
            camera_definitions = FFMPEGNVR.nvr_list.values()
            resp_obj = {
                "results": [response_generator.get_resp_obj(x, fields) for x in camera_definitions]
            }

            self.response_success(resp_obj)
            return
        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error(
                f"Error in API {self.__class__.__name__}.{kwargs['route']['method']}: "
                f"{str(error)}"
            )
            self.response_error(STATUS_ERROR_INTERNAL, reason=str(error))
