class MySql:
    def __init__(self):
        print("init")

    def __enter__(self):
        print("entering")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exiting")
