import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pydub import AudioSegment
import logging
import configparser


log_dir = "./logs"
# Create a custom logger
name = __name__
logger = logging.getLogger(name)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(os.path.join(log_dir, f"{name}.log"))
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

class Watcher:

    def __init__(self, config):
        self.config = config
        logger.info("Creating observer")
        self.observer = Observer()

    def run(self):
        logger.info("Creating Event Handler")
        event_handler = Handler()
        self.observer.schedule(
            event_handler,
            "/home/darkwing/Dokumente",
            recursive=False
        )
        logger.info("Starting observer")

        self.observer.start()
        try:
            while True:
                time.sleep(60)
        except:
            self.observer.stop()
            logger.error("An Error occured, stopping watcher")
        
        self.observer.join()


class Handler(PatternMatchingEventHandler):
    

    def on_created(self, event):
        print("New file found")
        logger.info("New file was created")
        logger.info("preparing to convert file")

        logger.debug("loading config file")
        config = configparser.ConfigParser()
        config.read("/home/darkwing/dev/file_watcher/config.ini")
        logger.debug("config file loaded")

        logger.info("Listing files in dir {}".format(config.get("System","location_to_watch")))
        data_in_dir = os.listdir("/home/darkwing/Dokumente")
        print(f"{data_in_dir}")
        logger.debug(f"{data_in_dir}")

        for each in data_in_dir:
            if each == "GOOD":
                print(each)
            else:
                print("Test")
                file_name, ext = each.split(".")
                print(f"getting filename: {file_name}")
                logger.debug(f"getting filename: {file_name}")

                try:
                    logger.debug(f"Trying to load wav file: {each}")
                    AudioSegment.from_wav(f"/home/darkwing/Dokumente/{file_name}.wav").export(f"/home/darkwing/Bilder/{file_name}.mp3", format="mp3")
                    logger.info(f"Wav-file: [{each}] successfully loaded")
                except Exception as e:
                    logger.error("Wav_file could not be loaded.")
                    logger.error(e)
                
                shutil.move(f"/home/darkwing/Dokumente/{file_name}.wav", "/home/darkwing/Dokumente/GOOD/")
