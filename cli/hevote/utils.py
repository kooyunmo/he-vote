import functools
import os
from enum import Enum
from pathlib import Path
from typing import Callable

import requests
import typer


BASE_URL = "http://localhost:8000/api"
CRED_PATH = os.path.join(os.environ["HOME"], ".hevote")
ACCESS_TOKEN_PATH = os.path.join(CRED_PATH, "access_token")
REFRESH_TOKEN_PATH = os.path.join(CRED_PATH, "refresh_token")


class TokenType(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


def get_url(path: str) -> str:
    return f"{BASE_URL}/{path}"


def update_token(token_type: TokenType, token: str) -> None:
    try:
        Path(CRED_PATH).mkdir(exist_ok=True)
    except (FileNotFoundError, FileExistsError) as e:
        secho_error_and_exit(f"Cannot store credential info... {e}")
    if token_type == TokenType.ACCESS:
        Path(ACCESS_TOKEN_PATH).write_text(token)
    elif token_type == TokenType.REFRESH:
        Path(REFRESH_TOKEN_PATH).write_text(token)


def get_token(token_type: TokenType) -> str | None:
    try:
        if token_type == TokenType.ACCESS:
            return Path(ACCESS_TOKEN_PATH).read_text()
        if token_type == TokenType.REFRESH:
            return Path(REFRESH_TOKEN_PATH).read_text()
        else:
            secho_error_and_exit("token_type should be one of 'access' or 'refresh'.")
    except FileNotFoundError:
        return None


def get_auth_header() -> dict:
    return {"Authorization": f"Bearer {get_token(TokenType.ACCESS)}"}


def secho_error_and_exit(text: str, color: str = typer.colors.RED):
    typer.secho(text, err=True, fg=color)
    raise typer.Exit(1)


def auto_token_refresh(func: Callable[..., requests.Response]) -> Callable[..., requests.Response]:
    @functools.wraps(func)
    def inner(*args, **kwargs) -> requests.Response:
        r = func(*args, **kwargs)
        if r.status_code == 401 or r.status_code == 403:
            refresh_token = get_token(TokenType.REFRESH)
            if refresh_token is not None:
                refresh_r = requests.post(get_url("token/refresh/"), data={"refresh": refresh_token})
                try:
                    refresh_r.raise_for_status()
                except requests.HTTPError:
                    secho_error_and_exit("Failed to refresh access token... Please login again")

                update_token(token_type=TokenType.ACCESS, token=refresh_r.json()["access"])
                if "files" in kwargs:
                    files = kwargs["files"]
                    for _, file_tuple in files.items():
                        for element in file_tuple:
                            if hasattr(element, "seek"):
                                element.seek(0)
                r = func(*args, **kwargs)
                r.raise_for_status()
            else:
                secho_error_and_exit("Failed to refresh access token... Please login again")
        else:
            r.raise_for_status()
        return r
    return inner
