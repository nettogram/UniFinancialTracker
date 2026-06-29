from textual.app import App, ComposeResult
from textual.containers import Center, VerticalScroll
from textual.widgets import Button, ContentSwitcher, Footer, Header, Label, ProgressBar

from datafunctions import add_week
from saveload import load_stats, refreshstats, save_stats


class FinanceTracker(App[None]):
    CSS_PATH = "styles.tcss"
    TITLE = "Uni Finance Tracker"
    BINDINGS = [("q", "quit_app", "Save and Quit App")]

    def compose(self) -> ComposeResult:
        yield Header()

        with ContentSwitcher(initial="semester-view"):
            with Center(id="semester-view"):
                yield Label("Current Semester Progress")
                yield ProgressBar(id="semprogress", show_eta=False)
                yield Label(id="sempercent-total")

            with Center(id="overall-view"):
                yield Label("Overall University Progress")
                yield ProgressBar(id="ovrprogress", show_eta=False)
                yield Label(id="ovrpercent-total")

        with Center():
            yield Button("Log Weekly Entry", id="pay-log")

        with Center(id="buttons"):
            yield Button("Semester View", id="semester-view")
            yield Button("Overall View", id="overall-view")

        yield VerticalScroll(id="history")

        yield Footer()

    def on_mount(self) -> None:
        self.savefile = "saves/savefiletest.json"
        self.user_info = load_stats(self.savefile)
        self.current_stats = refreshstats(self.user_info)

        self.ovrprogress = self.query_one("#ovrprogress", ProgressBar)
        self.ovrtotals = self.query_one("#ovrpercent-total", Label)
        self.semprogress = self.query_one("#semprogress", ProgressBar)
        self.semtotals = self.query_one("#sempercent-total", Label)

        self.semprogress.update(
            total=self.user_info["Semester Cost"],
            progress=(
                self.user_info["Semester Cost"]
                - self.current_stats["Semester Amount Due"]
            ),
        )

        self.semtotals.update(
            f"${self.current_stats['Current Semester Paid']} / ${self.user_info['Semester Cost']}"
        )

        self.ovrprogress.update(
            total=self.current_stats["Total Cost"],
            progress=self.current_stats["Tuition Paid"],
        )

        self.ovrtotals.update(
            f"${self.current_stats['Tuition Paid']} / ${self.current_stats['Total Cost']}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "overall-view":
            self.query_one(ContentSwitcher).current = "overall-view"
        elif event.button.id == "semester-view":
            self.query_one(ContentSwitcher).current = "semester-view"
        elif event.button.id == "pay-log":
            self.add_pay_entry()

    def add_pay_entry(self) -> None:
        self.current_stats = refreshstats(self.user_info)

        try:
            self.current_stats = add_week(self.user_info, self.current_stats)
        except ValueError:
            self.query_one(VerticalScroll).mount(
                Label("Invalid entry. Cannot log a standard payment yet")
            )
            return

        self.semprogress.update(
            progress=(
                self.user_info["Semester Cost"]
                - self.current_stats["Semester Amount Due"]
            )
        )
        self.ovrtotals.update(
            f"${self.current_stats['Tuition Paid']} / ${self.current_stats['Total Cost']}"
        )
        self.semtotals.update(
            f"${self.current_stats['Current Semester Paid']} / ${self.user_info['Semester Cost']}"
        )
        self.query_one(VerticalScroll).mount(
            Label(
                f"Logged another week into overall payments. Total Number of weeks paid: {self.current_stats['Times Paid']}"
            )
        )

    def action_quit_app(self) -> None:
        save_stats(self.savefile, self.user_info)
        self.exit()


if __name__ == "__main__":
    FinanceTracker().run()
