from enum import Enum

import requests
import typer
import plotext as plt
from rich.table import Table
from rich.console import Console

from hevote.cast import CastApp
from hevote.utils import (
    TokenType,
    auto_token_refresh,
    get_auth_header,
    get_url,
    secho_error_and_exit,
    update_token,
)


app = typer.Typer(
    help="Safe voting with homomorphic encryption",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=True
)


@app.command(help="Login")
def login(
    username: str = typer.Option(..., prompt="Enter Username"),
    password: str = typer.Option(..., prompt="Enter Password", hide_input=True)
):
    r = requests.post(get_url('token/'), data={'username': username, 'password': password})
    try:
        r.raise_for_status()
    except requests.HTTPError:
        secho_error_and_exit("Authentication failed...")

    update_token(token_type=TokenType.ACCESS, token=r.json()['access'])
    update_token(token_type=TokenType.REFRESH, token=r.json()['refresh'])
    typer.secho("Welcome!", fg=typer.colors.GREEN)


@auto_token_refresh
@app.command(help="Cast a vote")
def cast():
    try:
        CastApp.run(title="YOUR VOTE IS YOUR VOICE")
    except requests.HTTPError:
        secho_error_and_exit("Failed to cast a vote...")


class HEScheme(str, Enum):
    ASHE = "ashe"
    PAILLIER = "paillier"
    BFV = "bfv"


@auto_token_refresh
@app.command(help="Show results")
def result(
    scheme: HEScheme = typer.Option(
        HEScheme.ASHE,
        '-s',
        '--scheme'
    )
):
    r = requests.get(get_url('tally/'), headers=get_auth_header(), params={'cipher': scheme.value})
    try:
        r.raise_for_status()
    except requests.HTTPError:
        secho_error_and_exit("Failed to get results...")
    res = r.json()

    cands = ["Washington", "Adams", "Jefferson"]

    console = Console()
    table = Table(title="Vote result")
    for cand in cands:
        table.add_column(cand)

    votes = [ r['votes'] for r in res ]
    table.add_row(*list(map(str, votes)))
    console.print(table)

    total = sum(votes)
    vote_percents = [ v / total * 100 for v in votes ]

    plt.bar(cands, vote_percents)
    plt.clc()
    plt.plot_size(100, 60)
    plt.ylim(0, 100)
    plt.yfrequency(11)
    plt.title("Vote Result")
    plt.show()

    table = Table(title="Vote result")
    typer.secho(f"Latency: {res[0]['latency']:.5f}")


@auto_token_refresh
@app.command(help="Show results")
def compare():
    latencies = []
    for e in HEScheme:
        r = requests.get(get_url('tally/'), headers=get_auth_header(), params={'cipher': e.value})
        try:
            r.raise_for_status()
        except requests.HTTPError:
            secho_error_and_exit("Failed to get results...")
        res = r.json()
        latencies.append(res[0]['latency'])

    plt.bar([e.value for e in HEScheme], latencies, orientation='horizontal', width=3/5)
    plt.clc()
    plt.plot_size(100, 30)
    plt.title("Latency of HE schemes")
    plt.show()
