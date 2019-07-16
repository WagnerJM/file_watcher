import os
from watcher.watcher import Watcher
import configparser
from watcher.watcher import Handler
from watchdog.observers import Observer


def check_for_log_dir(config):
    if not os.path.exists(config.get('Logging','log_location')):
        print("Location does not exist, creating new log directory")
        os.mkdir(config.get("Log", "log_location"))
    else:
        print("Directory exists, nothing to do here.")

def main():
    config = configparser.ConfigParser()

    config.read("config.ini")
        
    #check_for_log_dir(config)
    w = Watcher(config)
    w.run()

if __name__ == '__main__':
    config = configparser.ConfigParser()

    config.read("config.ini")
    o = Observer()
    o.schedule(
        Handler(), 
        path=config['System']['location_to_watch']
        )
    o.start()

    try:
        while True:
            import time 
            time.sleep(1)
    except KeyboardInterrupt:
        o.stop()
    
    o.join()
