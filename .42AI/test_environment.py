import sys

REQUIRED_PYTHON = "python3.8"
required_major = 3
required_minor = 8


def main():
    system_major = sys.version_info.major
    system_minor = sys.version_info.minor
    print(
        f"Your current python version is python{sys.version_info.major}.{sys.version_info.minor}")

    if system_major != required_major:
        raise TypeError(
            "This project requires Python{}.{}. Found: Python{}.{}".format(
                required_major, required_minor, system_major, system_minor))
    elif system_minor != required_minor:
        raise TypeError(
            "This project requires Python{}.{}. Found: Python{}.{}".format(
                required_major, required_minor, system_major, system_minor))
    else:
        print(">>> Development environment passes all tests!")


if __name__ == '__main__':
    main()
