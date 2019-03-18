import click
import logging
from monitor import Config, start_working, setup_monitors


@click.command()
@click.option("--config", type=str, default="config.yaml")
@click.option("--monitor_interval", type=int, default=2)
@click.option("--multithreading", type=bool, default=False)
@click.option("--trigger_downtime", type=int, default=0)
@click.option("--silent", type=bool, default=False)
def main(**kwargs):
    Config.add_general_config(kwargs)

    log = logging.getLogger(__name__)

    Config.load_monitor_config()

    monitors = setup_monitors()  # Initiates Monitors

    start_working(monitors)


if __name__ == '__main__':
    main()
