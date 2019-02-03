import click
from monitor import Config, start_working, setup_monitors

@click.command()
@click.option("--config", type=str, default="config.yaml")
def main(config):
    # TODO COnfig Refactroing ware angemessen
    # TODO Multiple Monitors bug
    # TODO check compatibility for triggers might be useful for multiple sources
    """Also:
    group message print
    add BTS Support
    add database support for a public api
    Eine source d.h mache triggers und action als liste von einers source -> mehrere sources pro monitor
    _ uberall d.h. trigger.get_level
    monitor als threads ?"""

    Config.load_monitor_config(config)

    monitors = setup_monitors()  # Initiates Monitors

    print("{0} Monitor(s) added! Start Monitoring\n\n".format(len(monitors)))
    start_working(monitors)


if __name__ == '__main__':
    main()
