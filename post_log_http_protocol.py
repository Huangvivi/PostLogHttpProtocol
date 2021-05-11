from sanic.exceptions import InvalidUsage
from sanic.server import HttpProtocol
from sanic.response import HTTPResponse
from sanic.log import access_logger, logger


class PostLogHttpProtocol(HttpProtocol):
    # -------------------------------------------- #
    # Responding
    # -------------------------------------------- #
    def log_response(self, response):
        """
        Helper method provided to enable the logging of responses in case if
        the :attr:`HttpProtocol.access_log` is enabled.

        :param response: Response generated for the current request

        :type response: :class:`sanic.response.HTTPResponse` or
            :class:`sanic.response.StreamingHTTPResponse`

        :return: None
        """
        if self.access_log:
            extra = {"status": getattr(response, "status", 0)}

            if isinstance(response, HTTPResponse):
                extra["byte"] = len(response.body)
            else:
                extra["byte"] = -1

            extra["host"] = "UNKNOWN"
            if self.request is not None:
                if self.request.ip:
                    extra["host"] = f"{self.request.ip}:{self.request.port}"
                extra["request"] = f"{self.request.method} {self.request.url}"

                if self.request.body:
                    extra["body"] = f"{self.request.body}"
                    try:
                        if self.request.json:
                            extra["body"] = f"{self.request.json}"
                    except InvalidUsage:
                        pass
                    try:
                        if self.request.form:
                            extra["body"] = f"{self.request.form}"
                    except Exception:
                        pass
                else:
                    extra["body"] = ""

            else:
                extra["request"] = "nil"

            access_logger.info("", extra=extra)

