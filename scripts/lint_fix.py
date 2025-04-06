import subprocess


def main():
    """Runs all the necessary lint fix steps."""
    commands = [
        # Autoflake: Removes unused imports and variables
        "autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .",  # noqa: E501
        # isort: Sort imports
        "isort .",
        # Black: Format code
        "black .",
    ]

    for command in commands:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True)
