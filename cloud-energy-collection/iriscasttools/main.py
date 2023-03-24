"""
Collects energy usage metrics using IPMI, as well as other metrics such as CPU and RAM usage.
"""
import sys
import utils
import argparse


def get_iriscast_stats(csv=False, include_header=False):
    """
    Get stats for iriscast

    Keyword arguments:
        csv -- bool, flag to set if output should be formatted as csv or dict
        include_header -- bool, flag to set if header should be included if csv flag set

    """

    all_stats = {}

    power_stats = utils.get_ipmi_power_stats("current_power")

    all_stats.update(power_stats)
    all_stats.update(utils.get_os_load("os_load_5"))
    all_stats.update(utils.get_ram_usage("ram_usage_percentage"))

    if csv:
        return utils.to_csv(all_stats, include_header)
    return all_stats


def parse_args(inp_args):
    parser = argparse.ArgumentParser(
        prog="iriscasttools",
        description="colelcts current power usage for node using IPMI, as well as OS load and RAM usage",
    )
    parser.add_argument("-c", "--as-csv", default=False, action="store_true")
    parser.add_argument("-i", "--include-header", default=False, action="store_true")
    args, unknown = parser.parse_known_args(inp_args)

    # ignore include header if csv arg not set
    if args.include_header and not args.as_csv:
        args.include_header = False

    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    print(get_iriscast_stats(args.as_csv, args.include_header))
