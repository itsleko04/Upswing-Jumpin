from Assets import Application
from configparser import ConfigParser


def main():
    settings = ConfigParser()
    settings.read("settings.ini")
    app = Application(settings)
    app.run()


if __name__ == "__main__":
    main()