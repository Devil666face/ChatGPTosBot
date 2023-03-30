import subprocess


def answer(phrase):
    result = subprocess.Popen(
        f"sgpt '{phrase}'",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="UTF-8",
    )

    output, error = result.communicate()

    # Convert the output from bytes to a string and print it
    print(output)


if __name__ == "__main__":
    phrase = input()
    answer(phrase)
