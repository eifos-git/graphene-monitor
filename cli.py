import click
import logging
from monitor import Config, start_working, setup_monitors


@click.command()
@click.option("--config", type=str, default="config.yaml")
@click.option("--monitor_interval", type=int, default=2)
@click.option("--multithreading", type=bool, default=False)
def main(**kwargs):
    # TODO test monitor and test config schreiben
    # TODO There might be a way to outsource some things from the do_monitoring class especially everything from stp
    """Also:
    add database support for a public api
    A method to make the class names shorter might be useful
    Timestamp bock alter als 15 sec
    Event hochstens 120 inplay
    DNS tets
    graphene healthchecker config
    change console to stdout
    """

    Config.add_general_config(kwargs)

    log = logging.getLogger(__name__)

    Config.load_monitor_config()

    monitors = setup_monitors()  # Initiates Monitors

    start_working(monitors)


if __name__ == '__main__':
    main()
