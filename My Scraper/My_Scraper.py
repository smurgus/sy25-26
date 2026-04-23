import subprocess
import sys

def run_pip_command(args):
    """
    Runs a pip command with the provided arguments.
    Example: run_pip_command(['install', 'requests'])
    """
    if "exit" in args:
        return

    command = [sys.executable, '-m', 'pip'] + args
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)

if __name__ == "__main__":
    # Example usage: python PythonCommand.py install requests
    if len(sys.argv) < 2:
        print("Usage: python PythonCommand.py <pip-args>")
        print("Example: python PythonCommand.py install requests")
    else:
        run_pip_command(sys.argv[1:])

print("Enter your Python command below (e.g - \"install pygame\"). Use 'exit' to quit.")
cmd = input(">>> ")
run_pip_command(cmd.split(' '))

