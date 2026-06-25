from textual.app import App, ComposeResult
from textual.containers import Center, VerticalScroll
from textual.widgets import Button, Header, Input, Label, ProgressBar

from saveload import load_stats, refreshstats
from datafunctions import add_week

class FinanceTracker(App[None]):
    CSS_PATH = "styles.tcss"
    TITLE = "Uni Finance Tracker"

    def compose(self) -> ComposeResult:
        savefile = "saves/savefiletest.json"
        user_info = load_stats(savefile)
        current_stats = refreshstats(user_info)
        progress = ProgressBar(
            total=user_info["Semester Cost"],
            show_eta=False,
        )
        progress.update(
            progress=(user_info["Semester Cost"] - current_stats["Semester Amount Due"])
        )
        yield Header()
        with Center():
            yield Label("Current Semester Progress")
            yield progress
        with Center():
            yield Button("Log Weekly Entry")

        yield VerticalScroll(id="history")

    def on_mount(self) -> None:

    def on_button_pressed(self) -> None:
        self.add_pay_entry()

    def on_input_submitted(self) -> None:
        self.add_pay_entry()

    def add_pay_entry(self) -> None:
        savefile = "saves/savefiletest.json"
        user_info = load_stats(savefile)
        current_stats = refreshstats(user_info)
        current_stats = add_week(user_info, current_stats)
        progress.update(
            progress=(user_info["Semester Cost"] - current_stats["Semester Amount Due"])
        )
        self.query_one(VerticalScroll).mount(
            Label(f"Logged another week into overall payments!")
        )


if __name__ == "__main__":
    FinanceTracker().run()
