from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    Collapsible,
    ContentSwitcher,
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    ProgressBar,
    RichLog,
    Static,
)

from datafunctions import add_week
from saveload import load_stats, refreshstats, save_stats

# Base directory for the position of current file
BASE_DIR = Path(__file__).resolve().parent


# App that controls the entire finance tracker program
class FinanceTracker(App[None]):
    # Initial calls. Links to CSS path, Title, and quit binding for later
    CSS_PATH = "styles.tcss"
    TITLE = "Uni Finance Tracker"
    BINDINGS = [("q", "quit_app", "Save and Quit App")]

    # Compose comprises of 3 layers: Top, Content, Buttons. Each linked by ID
    # Compose controls the layout and declaration of widgets for the application
    def compose(self) -> ComposeResult:
        semester = Container(id="semester-view")
        semester.border_title = "Current Semester Progress"
        overall = Container(id="overall-view")
        overall.border_title = "Overall University Progress"
        logfield = Horizontal(id="logocontainer")
        logfield.border_title = "Sacramento State - ECS"
        logfield.border_subtitle = "History Log"
        yield Header()

        with Vertical():
            # First stack
            with Container(id="top-row"):
                yield Button("Log Weekly Entry", id="pay-log")

            # Second stack
            with Horizontal(id="content-row"):
                with Center():
                    with ContentSwitcher(initial="semester-view"):
                        with semester:
                            with Center():
                                yield ProgressBar(id="semprogress", show_eta=False)
                                yield Label(id="sempercent-total")
                        with overall:
                            with Center():
                                yield ProgressBar(id="ovrprogress", show_eta=False)
                                yield Label(id="ovrpercent-total")

                with Center():
                    with Collapsible(title="Additional Stats", id="extrastats"):
                        yield ListView(
                            ListItem(Label("Weeks Paid", id="payweeks")),
                            ListItem(Label("Semester Counter", id="semcount")),
                        )

            # Third Stack
            with Horizontal(id="buttons"):
                yield Button("Semester View", id="semester-button")
                yield Button("Overall View", id="overall-button")

            # Fourth Stack
            with logfield:
                with Center():
                    LOGO_FILE = BASE_DIR / "assets" / "sacstatelogo.txt"
                    yield Static(LOGO_FILE.read_text(), id="logo")
                with VerticalScroll():
                    yield RichLog(id="historylog")

        yield Footer()

    # On mount is the actions that are performed as soon as the application starts
    def on_mount(self) -> None:
        # Three main "globals". These control the backend
        self.savefile = BASE_DIR / "saves" / "savefiletest.json"
        self.user_info = load_stats(self.savefile)
        self.current_stats = refreshstats(self.user_info)

        # Quick janky fix to not auto focus on startup without an interaction
        self.query_one("#pay-log", Button).blur()

        # For runtime changes to ProgressBar and Fractional view
        self.ovrprogress = self.query_one("#ovrprogress", ProgressBar)
        self.ovrtotals = self.query_one("#ovrpercent-total", Label)
        self.semprogress = self.query_one("#semprogress", ProgressBar)
        self.semtotals = self.query_one("#sempercent-total", Label)

        # For additional stats
        self.payweeks = self.query_one("#payweeks", Label)
        self.semcount = self.query_one("#semcount", Label)

        # For the log
        self.historylog = self.query_one("#historylog", RichLog)

        # to update stats on startup
        self.update_stats()

    def update_stats(self) -> None:
        # Updates values to be shown on screen.
        # Section for Semester:
        self.semprogress.update(
            total=(self.user_info["Semester Cost"]),
            progress=(
                self.user_info["Semester Cost"]
                - self.current_stats["Semester Amount Due"]
            ),
        )
        self.semtotals.update(
            f"${self.current_stats['Current Semester Paid']} / ${self.user_info['Semester Cost']}"
        )
        # Section for Overall:
        self.ovrprogress.update(
            total=self.current_stats["Total Cost"],
            progress=self.current_stats["Tuition Paid"],
        )
        self.ovrtotals.update(
            f"${self.current_stats['Tuition Paid']} / ${self.current_stats['Total Cost']}"
        )
        # Immediate update on mount for additional stats
        self.payweeks.update(f"Weeks Paid: {self.current_stats['Times Paid']}")
        self.semcount.update(
            f"Semesters Paid for: {self.current_stats['Semester Counter']}"
        )

    # Controls all button presses
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Links button switches to view switches
        if event.button.id == "overall-button":
            self.query_one(ContentSwitcher).current = "overall-view"
        elif event.button.id == "semester-button":
            self.query_one(ContentSwitcher).current = "semester-view"
        # Links payment button to pay entry definition
        elif event.button.id == "pay-log":
            self.add_pay_entry()

    def add_pay_entry(self) -> None:
        # Immediate stat refresh before any action to ensure what will be acted on is the current stats
        self.current_stats = refreshstats(self.user_info)

        # The main action to change stats on JSON
        try:
            self.current_stats = add_week(self.user_info, self.current_stats)
        except ValueError:
            self.historylog.write(
                Text.from_markup(
                    "[red] ERROR with adding entry. Use the CLI Debugger for diagnostics[/red]"
                )
            )
            return
        else:
            if self.current_stats["Entry Status"] == "FAIL":
                self.historylog.write(
                    Text.from_markup(
                        "[red]Invalid entry. Cannot log a standard payment yet[/red]"
                    )
                )
            else:
                # Updates stats on call of add_pay_entry()
                self.update_stats()

                # Adds log and also Total # of weeks. Will make a dropdown for stats in the future
                self.historylog.write(
                    Text.from_markup(
                        f"[green]Logged another week into overall payments. Total Number of weeks paid:[/green][yellow] {self.current_stats['Times Paid']}[/yellow]"
                    )
                )

    # When 'q' is pressed, everything saves and the application is exited
    def action_quit_app(self) -> None:
        save_stats(self.savefile, self.user_info)
        self.exit()


def main() -> None:
    app = FinanceTracker()
    app.run()


if __name__ == "__main__":
    main()
