import os
from watcher.watcher import watcher
import configparser


def check_for_log_dir(config):
    if not os.path.exists(config.get('Log','log_location')):
        print("Location does not exist, creating new log directory")
        os.mkdir(config.get("Log", "log_location"))
    else:
        print("Directory exists, nothing to do here.")

def main():
    config = configparser.ConfigParser()

    try:
        config.read("config.ini")
    except Exception as e:
        print("Config file not found")
        print(e)
        
    check_for_log_dir(config)
    w = Watcher(config)
    w.run()

if __name__ == '__main__':
    main()