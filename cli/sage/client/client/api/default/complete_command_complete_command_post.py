from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.retrieval_and_output import RetrievalAndOutput
from ...types import UNSET, Response


def _get_kwargs(
    *,
    prompt: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["prompt"] = prompt

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/complete_command",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, RetrievalAndOutput]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RetrievalAndOutput.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, RetrievalAndOutput]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    prompt: str,
) -> Response[Union[HTTPValidationError, RetrievalAndOutput]]:
    """Complete Command

     Based on prompt. Returns the top relevant commands or suggest one if none found

    Args:
        prompt (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RetrievalAndOutput]]
    """

    kwargs = _get_kwargs(
        prompt=prompt,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    prompt: str,
) -> Optional[Union[HTTPValidationError, RetrievalAndOutput]]:
    """Complete Command

     Based on prompt. Returns the top relevant commands or suggest one if none found

    Args:
        prompt (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RetrievalAndOutput]
    """

    return sync_detailed(
        client=client,
        prompt=prompt,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    prompt: str,
) -> Response[Union[HTTPValidationError, RetrievalAndOutput]]:
    """Complete Command

     Based on prompt. Returns the top relevant commands or suggest one if none found

    Args:
        prompt (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RetrievalAndOutput]]
    """

    kwargs = _get_kwargs(
        prompt=prompt,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    prompt: str,
) -> Optional[Union[HTTPValidationError, RetrievalAndOutput]]:
    """Complete Command

     Based on prompt. Returns the top relevant commands or suggest one if none found

    Args:
        prompt (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RetrievalAndOutput]
    """

    return (
        await asyncio_detailed(
            client=client,
            prompt=prompt,
        )
    ).parsed
