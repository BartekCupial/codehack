from importlib.resources import files


def des_file(name: str) -> str:
    return str(files("codehack").joinpath("envs", "minihack", "dat", name))
