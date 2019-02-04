import click
import logging
from monitor import Config, start_working, setup_monitors


@click.command()
@click.option("--config", type=str, default="config.yaml")
@click.option("--monitor_interval", type=int, default=2)
@click.option("--multithreading", type=bool, default=False)
@click.option("--downtime", type=int, default=1)
def main(**kwargs):
    # TODO: Debug downtime length. It doesnt work yet. _last_time_fired is always None
    # TODO check compatibility for triggers might be useful for multiple sources
    # TODO write some nice test cases. AbstractTrigger.fired_recently() might have caused trouble
    """Also:
    add database support for a public api
    A method to make the class names shorter might be useful
    Interval trigger
    Add triggers.check_compatability
    Timestamp bock älter als 15 sec
    Event höchstens 120 inplay
    DNS tets
    graphene healthchecker config
    change console to stdout
    """

    Config.add_general_config(kwargs)

    log = logging.getLogger(__name__)

    Config.load_monitor_config()

    monitors = setup_monitors()  # Initiates Monitors

    print("{0} Monitor(s) added! Start Monitoring\n\n".format(len(monitors)))
    start_working(monitors)


if __name__ == '__main__':
    main()
