import questionary

class NeurobikTUI:
    """Simple TUI for selecting downloads using questionary."""

    def __init__(self, items):
        self.items = items  # List of dicts with 'name', 'type'

    def run(self):
        print(r"""
╭─═══════════════════════════════════════════════════════════════════════════─╮
                   _   _                      _     _ _
                  | \ | | ___ _   _ _ __ ___ | |__ (_) | __
                  |  \| |/ _ \ | | | '__/ _ \| '_ \| | |/ /
                  | |\  |  __/ |_| | | | (_) | |_) | |   <
                  |_| \_|\___|\__,_|_|  \___/|_.__/|_|_|\_\

                         The premier thawing agent. 
╰─═══════════════════════════════════════════════════════════════════════════─╯
""")
    
        choices = [f"{item['type']}: {item['name']}" for item in self.items]
        selected_indices = questionary.checkbox("Select items to download:", choices).ask()
        if selected_indices:
            selected = [self.items[choices.index(choice)] for choice in selected_indices]
            return selected
        return []
