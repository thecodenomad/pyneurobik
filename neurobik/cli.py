import click
import os
from neurobik.config import Config
from neurobik.tui import NeurobikTUI
from neurobik.downloader import Downloader
from neurobik.utils import setup_logging
import sys

@click.command()
@click.option('--config', required=True, help='Path to YAML config file')
def download(config):
    """Download models and OCI images based on config."""
    logger = setup_logging()
    try:
        cfg = Config.from_yaml(config)
        Downloader.check_podman()

        # Prepare items for TUI - only show models that haven't been downloaded yet
        items = []
        for model in cfg.models:
            if not os.path.exists(model.confirmation_file):
                items.append({'name': model.model_name, 'type': 'model'})
        for oci in cfg.oci:
            items.append({'name': oci.image, 'type': 'oci'})

        if not items:
            click.echo("No items to download.")
            return

        # Launch TUI
        tui = NeurobikTUI(items)
        selected = tui.run()

        print("""
╭─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╮
┊                           🚀 Downloads Starting...                          ┊
╰─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╯\n""")

        downloader = Downloader()
        downloaded_models = []
        for item in selected:
            if item['type'] == 'model':
                model = next(m for m in cfg.models if m.model_name == item['name'])
                downloader.pull_model(cfg.model_provider, model.repo_name, model.model_name, model.location, model.confirmation_file)
                downloaded_models.append(model)
            elif item['type'] == 'oci':
                oci = next(o for o in cfg.oci if o.image == item['name'])
                downloader.pull_oci(oci.image, oci.confirmation_file, oci.containerfile, oci.build_args)

        # Create default symlink if any models were downloaded
        if downloaded_models:
            first_model = downloaded_models[0]
            models_dir = os.path.dirname(first_model.confirmation_file)
            downloader.create_default_symlink(models_dir, first_model.location)
            print(f"Default model (first in config): {first_model.location}")

        # Create confirmation files after symlinking
        from neurobik.utils import create_confirmation_file
        for model in downloaded_models:
            create_confirmation_file(model.confirmation_file)

        # Create provider confirmation file if any models were downloaded
        if downloaded_models and cfg.provider_confirmation_file:
            create_confirmation_file(cfg.provider_confirmation_file)

        print(r"""
╭─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╮                
┊          🎉 All Downloads Complete - Your AI Overlords Approve! 🎉          ┊
╰─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╯

╭─═══════════════════════════════════════════════════════════════════════════─╮
                                                           ·◎◎··●·           
                                                        ·○○··········        
                                                      ·◎········· ····       
                                                     ·················●      
                                                     ··········     ····     
                                                  ··◉○·○······      ···○○·   
                                                ·○○○○·○○············  ··◎·   
                                              ·○○◉···○○◉· ···············    
                                        ●◉◉●○···◉·····○○···   ········○·     
                                        ●◉◉◉··        ●················      
                                       ◉○◎◎○○·○◎·      ··○··  ····●···       
           _ _                      ··●·○●◉◉◎◎◎◎◎●       ··●···●·            
      _   _| |__ (_) | __           ·◉○○◎◎◎◎◎○··○◎                           
     | | | | '_ \| | |/ /           ·◉○○◎◎◎◎◎○··○◎●·                         
     | |_| | |_) | |   <            ·●○·○◎◎◎◎◎○··○◉·                         
      \__,_|_.__/|_|_|\_\           ··◎·○◎◎◎◎◎○··○◎·                         
                                      ◉○○◎◎◎◎◎◎○··◎●·                        
     Safe when used as directed.      ·◎·○◎◎◎◎◎○··○◉·                        
                                      ·◎·○◎◎◎◎◎○○·○◎◎                        
                                       ●○·○◎◎◎◎◎○··◎◉·                       
                                       ·◎·○◎◎◎◎◎○··○◎·                       
                                        ◉○○◎◎◎◎◎◎○·○◎●                       
                                        ●○·○◎◎◎◎◎○··○◉·                      
                                        ·◎·○◎◎◎◎◎○○·○◎·                      
                                         ◉○○○◎◎◎◎◎○○○◎◉                      
                                         ·◎○○◎◎◎◎◎○○○○◎·                     
                                         ·◉○○◎◎◎◎◎○○◉○◎·                     
                                          ●○○○○◎●○··                         
╰─═══════════════════════════════════════════════════════════════════════════─╯""")
        

    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    download()
