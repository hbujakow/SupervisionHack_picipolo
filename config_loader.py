import json

def load_config(filename: str = "config.json",) -> dict:
    f = open(filename)

    return json.load(f)


# TODO add argparser for custom config parser,
# and combining default config and argparse arguments