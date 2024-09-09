import os 

class WaterCycleCommandException(Exception):
    pass

def run_command(command: str) -> None:
    code = os.system(command)
    if code != 0:
        raise WaterCycleCommandException(f"Command {command} failed with code {code}")