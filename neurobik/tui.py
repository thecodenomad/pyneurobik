"""Terminal User Interface module for Neurobik.

This module provides a simple interactive interface for selecting
AI models and OCI containers to download using questionary.
"""

import questionary


class NeurobikTUI:  # pylint: disable=too-few-public-methods
    """Simple TUI for selecting downloads using questionary."""

    def __init__(self, items):
        """Initialize TUI with list of downloadable items."""
        self.items = items  # List of dicts with 'name', 'type'

    def run(self):
        """Run the interactive selection interface and return selected items."""
        print(
            r"""
╭─═══════════════════════════════════════════════════════════════════════════─╮
                   _   _                      _     _ _
                  | \ | | ___ _   _ _ __ ___ | |__ (_) | __
                  |  \| |/ _ \ | | | '__/ _ \| '_ \| | |/ /
                  | |\  |  __/ |_| | | | (_) | |_) | |   <
                  |_| \_|\___|\__,_|_|  \___/|_.__/|_|_|\_\

                         The premier thawing agent.
╰─═══════════════════════════════════════════════════════════════════════════─╯
"""
        )

        choices = [f"{item['type']}: {item['name']}" for item in self.items]
        selected_indices = questionary.checkbox("Select items to download:", choices).ask()
        if selected_indices:
            selected = [self.items[choices.index(choice)] for choice in selected_indices]
            return selected
        return []
