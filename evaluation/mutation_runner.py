import subprocess

def run_mutation():

    try:

        result = subprocess.run(
            ["mutmut", "run"],
            capture_output=True,
            text=True
        )

        return result.stdout

    except Exception as e:

        return {
            "error":str(e)
        }