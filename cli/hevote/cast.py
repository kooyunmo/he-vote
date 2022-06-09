import requests
from rich.panel import Panel
from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Footer, Header
from pyfiglet import Figlet

from hevote.utils import get_auth_header, get_url, secho_error_and_exit


class FigletText:
    """A renderable to generate figlet text that adapts to fit the container."""

    def __init__(self, text: str) -> None:
        self.text = text

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Build a Rich renderable to render the Figlet text."""
        size = min(options.max_width / 2, options.max_height)
        if size < 4:
            yield Text(self.text, style="bold")
        else:
            if size < 7:
                font_name = "mini"
            elif size < 8:
                font_name = "small"
            elif size < 10:
                font_name = "standard"
            else:
                font_name = "big"
            font = Figlet(font=font_name, width=options.max_width)
            yield Text(font.renderText(self.text).rstrip("\n"), style="bold")


class Hover(Widget):
    mouse_over = Reactive(False)

    def render(self) -> Panel:
        return Panel(FigletText(self.name), style=("bold black on white" if self.mouse_over else ""))

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

    def on_click(self) -> None:
        name_candidate_id = {
            'Washington': 1,
            'Adams': 2,
            'Jefferson': 3,
        }
        r = requests.post(
            get_url('cast/'),
            headers=get_auth_header(),
            json={'candidate_id': name_candidate_id[self.name]}
        )
        r.raise_for_status()
        exit(0)


class CastApp(App):
    async def on_load(self) -> None:
        """Bind keys here."""
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        """Build layout here."""
        header = Header()
        footer = Footer()

        await self.view.dock(header, edge="top")
        await self.view.dock(footer, edge="bottom")
        hovers = (Hover("Washington"), Hover("Adams"), Hover("Jefferson"))
        await self.view.dock(*hovers)
