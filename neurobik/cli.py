"""Command-line interface for Neurobik.

This module provides the main CLI entry point for downloading AI models
and OCI containers based on YAML configuration files.
"""

import os
import sys

import click
from neurobik.config import Config
from neurobik.downloader import Downloader
from neurobik.tui import NeurobikTUI
from neurobik.utils import create_confirmation_file, setup_logging


def _download_model(cfg, downloader, item, downloaded_models):
    """Download a single AI model and add it to the downloaded list.

    Args:
        cfg: Configuration object
        downloader: Downloader instance
        item: Dictionary with 'name' and 'type' keys
        downloaded_models: List to append downloaded model to
    """
    model = next(m for m in cfg.models if m.model_name == item["name"])
    downloader.pull_model(
        cfg.model_provider,
        model.repo_name,
        model.model_name,
        model.location,
        model.confirmation_file,
    )
    downloaded_models.append(model)


def _download_oci(cfg, downloader, item):
    """Download or build a single OCI container.

    Args:
        cfg: Configuration object
        downloader: Downloader instance
        item: Dictionary with 'name' and 'type' keys
    """
    oci = next(o for o in cfg.oci if o.image == item["name"])
    downloader.pull_oci(oci.image, oci.confirmation_file, oci.containerfile, oci.build_args)


@click.command()
@click.option("--config", required=True, help="Path to YAML config file")
def download(config):
    """Download models and OCI images based on config.

    Args:
        config: Path to YAML configuration file containing model and OCI definitions
    """
    logger = setup_logging()
    try:
        cfg = Config.from_yaml(config)
        Downloader.check_podman()

        # Prepare items for TUI - only show models that haven't been downloaded yet
        items = []
        for model in cfg.models:
            if not os.path.exists(model.confirmation_file):
                items.append({"name": model.model_name, "type": "model"})
        for oci in cfg.oci:
            items.append({"name": oci.image, "type": "oci"})

        if not items:
            click.echo("No items to download.")
            return

        # Launch TUI
        tui = NeurobikTUI(items)
        selected = tui.run()

        print(
            """
╭─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╮
┊                           🚀 Downloads Starting...                          ┊
╰─┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈─╯\n"""
        )

        downloader = Downloader()

        # Process selected items
        downloaded_models = []
        for item in selected:
            if item["type"] == "model":
                _download_model(cfg, downloader, item, downloaded_models)
            else:
                _download_oci(cfg, downloader, item)

        # Create default symlink if any models were downloaded
        if downloaded_models:
            default_model = next(
                (m for m in cfg.models if m.model_name == cfg.default_gguf),
                cfg.models[0]  # first in config if no default_gguf
            )
            models_dir = os.path.dirname(default_model.confirmation_file)
            downloader.create_default_symlink(models_dir, default_model.location)
            print(f"Default model: {default_model.location}")

        # Create confirmation files after symlinking
        for model in downloaded_models:
            create_confirmation_file(model.confirmation_file)

        # Create provider confirmation file if any models were downloaded
        if downloaded_models and cfg.provider_confirmation_file:
            create_confirmation_file(cfg.provider_confirmation_file)

        print(
            r"""
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
╰─═══════════════════════════════════════════════════════════════════════════─╯"""
        )

    except (ValueError, OSError, RuntimeError) as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    download()  # pylint: disable=no-value-for-parameter
