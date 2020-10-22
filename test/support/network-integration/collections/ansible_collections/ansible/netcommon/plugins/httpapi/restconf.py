# Copyright (c) 2018 Cisco and/or its affiliates.
#
# This file is part of Assible
#
# Assible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Assible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Assible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """author: Assible Networking Team
httpapi: restconf
short_description: HttpApi Plugin for devices supporting Restconf API
description:
- This HttpApi plugin provides methods to connect to Restconf API endpoints.
options:
  root_path:
    type: str
    description:
    - Specifies the location of the Restconf root.
    default: /restconf
    vars:
    - name: assible_httpapi_restconf_root
"""

import json

from assible.module_utils._text import to_text
from assible.module_utils.connection import ConnectionError
from assible.module_utils.six.moves.urllib.error import HTTPError
from assible.plugins.httpapi import HttpApiBase


CONTENT_TYPE = "application/yang-data+json"


class HttpApi(HttpApiBase):
    def send_request(self, data, **message_kwargs):
        if data:
            data = json.dumps(data)

        path = "/".join(
            [
                self.get_option("root_path").rstrip("/"),
                message_kwargs.get("path", "").lstrip("/"),
            ]
        )

        headers = {
            "Content-Type": message_kwargs.get("content_type") or CONTENT_TYPE,
            "Accept": message_kwargs.get("accept") or CONTENT_TYPE,
        }
        response, response_data = self.connection.send(
            path, data, headers=headers, method=message_kwargs.get("method")
        )

        return handle_response(response, response_data)


def handle_response(response, response_data):
    try:
        response_data = json.loads(response_data.read())
    except ValueError:
        response_data = response_data.read()

    if isinstance(response, HTTPError):
        if response_data:
            if "errors" in response_data:
                errors = response_data["errors"]["error"]
                error_text = "\n".join(
                    (error["error-message"] for error in errors)
                )
            else:
                error_text = response_data

            raise ConnectionError(error_text, code=response.code)
        raise ConnectionError(to_text(response), code=response.code)

    return response_data
