from packages.controllers.application import ApplicationController


def main():
    """ Programme principal """
    app = ApplicationController()
    app.start_app()


if __name__ == "__main__":
    main()
