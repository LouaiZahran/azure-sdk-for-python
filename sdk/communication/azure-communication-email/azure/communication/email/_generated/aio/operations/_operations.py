# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import sys
from typing import Any, Callable, Dict, IO, Optional, TypeVar, Union, cast, overload

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict

from ...operations._operations import build_email_get_send_status_request, build_email_send_request

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping  # type: ignore  # pylint: disable=ungrouped-imports
JSON = MutableMapping[str, Any]  # pylint: disable=unsubscriptable-object
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class EmailOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.communication.email.aio.AzureCommunicationEmailService`'s
        :attr:`email` attribute.
    """

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace_async
    async def get_send_status(self, message_id: str, **kwargs: Any) -> JSON:
        """Gets the status of a message sent previously.

        Gets the status of a message sent previously.

        :param message_id: System generated message id (GUID) returned from a previous call to send
         email. Required.
        :type message_id: str
        :return: JSON object
        :rtype: JSON
        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. code-block:: python

                # response body for status code(s): 200
                response == {
                    "messageId": "str",  # System generated id of an email message sent.
                      Required.
                    "status": "str"  # The type indicating the status of a request. Required.
                      Known values are: "queued", "outForDelivery", and "dropped".
                }
        """
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls = kwargs.pop("cls", None)  # type: ClsType[JSON]

        request = build_email_get_send_status_request(
            message_id=message_id,
            api_version=self._config.api_version,
            headers=_headers,
            params=_params,
        )
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, "str", skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        response_headers = {}
        response_headers["Retry-After"] = self._deserialize("int", response.headers.get("Retry-After"))

        if response.content:
            deserialized = response.json()
        else:
            deserialized = None

        if cls:
            return cls(pipeline_response, cast(JSON, deserialized), response_headers)

        return cast(JSON, deserialized)

    @overload
    async def send(  # pylint: disable=inconsistent-return-statements
        self,
        email_message: JSON,
        *,
        repeatability_request_id: str,
        repeatability_first_sent: str,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> None:
        """Queues an email message to be sent to one or more recipients.

        Queues an email message to be sent to one or more recipients.

        :param email_message: Message payload for sending an email. Required.
        :type email_message: JSON
        :keyword repeatability_request_id: If specified, the client directs that the request is
         repeatable; that is, that the client can make the request multiple times with the same
         Repeatability-Request-Id and get back an appropriate response without the server executing the
         request multiple times. The value of the Repeatability-Request-Id is an opaque string
         representing a client-generated, globally unique for all time, identifier for the request. It
         is recommended to use version 4 (random) UUIDs. Required.
        :paramtype repeatability_request_id: str
        :keyword repeatability_first_sent: Must be sent by clients to specify that a request is
         repeatable. Repeatability-First-Sent is used to specify the date and time at which the request
         was first created in the IMF-fix date form of HTTP-date as defined in RFC7231. eg- Tue, 26 Mar
         2019 16:06:51 GMT. Required.
        :paramtype repeatability_first_sent: str
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: None
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. code-block:: python

                # JSON input template you can fill out and use as your body input.
                email_message = {
                    "content": {
                        "subject": "str",  # Subject of the email message. Required.
                        "html": "str",  # Optional. Html version of the email message.
                        "plainText": "str"  # Optional. Plain text version of the email
                          message.
                    },
                    "recipients": {
                        "to": [
                            {
                                "email": "str",  # Email address. Required.
                                "displayName": "str"  # Optional. Email display name.
                            }
                        ],
                        "CC": [
                            {
                                "email": "str",  # Email address. Required.
                                "displayName": "str"  # Optional. Email display name.
                            }
                        ],
                        "bCC": [
                            {
                                "email": "str",  # Email address. Required.
                                "displayName": "str"  # Optional. Email display name.
                            }
                        ]
                    },
                    "sender": "str",  # Sender email address from a verified domain. Required.
                    "attachments": [
                        {
                            "attachmentType": "str",  # The type of attachment file.
                              Required. Known values are: "avi", "bmp", "doc", "docm", "docx", "gif",
                              "jpeg", "mp3", "one", "pdf", "png", "ppsm", "ppsx", "ppt", "pptm",
                              "pptx", "pub", "rpmsg", "rtf", "tif", "txt", "vsd", "wav", "wma", "xls",
                              "xlsb", "xlsm", and "xlsx".
                            "contentBytesBase64": "str",  # Base64 encoded contents of
                              the attachment. Required.
                            "name": "str"  # Name of the attachment. Required.
                        }
                    ],
                    "disableUserEngagementTracking": bool,  # Optional. Indicates whether user
                      engagement tracking should be disabled for this request if the resource-level
                      user engagement tracking setting was already enabled in the control plane.
                    "headers": [
                        {
                            "name": "str",  # Header name. Required.
                            "value": "str"  # Header value. Required.
                        }
                    ],
                    "importance": "normal",  # Optional. Default value is "normal". The
                      importance type for the email. Known values are: "high", "normal", and "low".
                    "replyTo": [
                        {
                            "email": "str",  # Email address. Required.
                            "displayName": "str"  # Optional. Email display name.
                        }
                    ]
                }
        """

    @overload
    async def send(  # pylint: disable=inconsistent-return-statements
        self,
        email_message: IO,
        *,
        repeatability_request_id: str,
        repeatability_first_sent: str,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> None:
        """Queues an email message to be sent to one or more recipients.

        Queues an email message to be sent to one or more recipients.

        :param email_message: Message payload for sending an email. Required.
        :type email_message: IO
        :keyword repeatability_request_id: If specified, the client directs that the request is
         repeatable; that is, that the client can make the request multiple times with the same
         Repeatability-Request-Id and get back an appropriate response without the server executing the
         request multiple times. The value of the Repeatability-Request-Id is an opaque string
         representing a client-generated, globally unique for all time, identifier for the request. It
         is recommended to use version 4 (random) UUIDs. Required.
        :paramtype repeatability_request_id: str
        :keyword repeatability_first_sent: Must be sent by clients to specify that a request is
         repeatable. Repeatability-First-Sent is used to specify the date and time at which the request
         was first created in the IMF-fix date form of HTTP-date as defined in RFC7231. eg- Tue, 26 Mar
         2019 16:06:51 GMT. Required.
        :paramtype repeatability_first_sent: str
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: None
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def send(  # pylint: disable=inconsistent-return-statements
        self,
        email_message: Union[JSON, IO],
        *,
        repeatability_request_id: str,
        repeatability_first_sent: str,
        **kwargs: Any
    ) -> None:
        """Queues an email message to be sent to one or more recipients.

        Queues an email message to be sent to one or more recipients.

        :param email_message: Message payload for sending an email. Is either a model type or a IO
         type. Required.
        :type email_message: JSON or IO
        :keyword repeatability_request_id: If specified, the client directs that the request is
         repeatable; that is, that the client can make the request multiple times with the same
         Repeatability-Request-Id and get back an appropriate response without the server executing the
         request multiple times. The value of the Repeatability-Request-Id is an opaque string
         representing a client-generated, globally unique for all time, identifier for the request. It
         is recommended to use version 4 (random) UUIDs. Required.
        :paramtype repeatability_request_id: str
        :keyword repeatability_first_sent: Must be sent by clients to specify that a request is
         repeatable. Repeatability-First-Sent is used to specify the date and time at which the request
         was first created in the IMF-fix date form of HTTP-date as defined in RFC7231. eg- Tue, 26 Mar
         2019 16:06:51 GMT. Required.
        :paramtype repeatability_first_sent: str
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :return: None
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        content_type = kwargs.pop("content_type", _headers.pop("Content-Type", None))  # type: Optional[str]
        cls = kwargs.pop("cls", None)  # type: ClsType[None]

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(email_message, (IO, bytes)):
            _content = email_message
        else:
            _json = email_message

        request = build_email_send_request(
            repeatability_request_id=repeatability_request_id,
            repeatability_first_sent=repeatability_first_sent,
            content_type=content_type,
            api_version=self._config.api_version,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, "str", skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        response_headers = {}
        response_headers["Repeatability-Result"] = self._deserialize(
            "str", response.headers.get("Repeatability-Result")
        )
        response_headers["Operation-Location"] = self._deserialize("str", response.headers.get("Operation-Location"))
        response_headers["Retry-After"] = self._deserialize("int", response.headers.get("Retry-After"))
        response_headers["x-ms-request-id"] = self._deserialize("str", response.headers.get("x-ms-request-id"))

        if cls:
            return cls(pipeline_response, None, response_headers)
