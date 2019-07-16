import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pydub import AudioSegment
import logging

config = configparser.ConfigParser()
config.read("../config.ini")
log_dir = config.get("Logging", "log_location")
# Create a custom logger
name = __name__
logging.getLogger(name)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(os.path.join(log_dir, f"{name}.log"))
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logging.addHandler(c_handler)
logging.addHandler(f_handler)

class Watcher:
    DIRECTORY_TO_WATCH = "/media/festplatte/public/recordings/input"
    OUTPUT_DIR = "/media/festplatte/public/recordings/output"

    def __init__(self, config):
        self.config = config
        logger.info("Creating observer")
        self.observer = Observer()

    def run(self):
        logger.info("Creating Event Handler")
        event_handler = Handler()
        self.observer.schedule(
            event_handler,
            self.DIRECTORY_TO_WATCH,
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

    def on_create(self, event):
        logging.info("New file was created")
        logging.info("preparing to convert file")

        logging.debug("loading config file")
        config = configparser.ConfigParser()
        config.read("../config.ini")
        logging.debug("config file loaded")

        logging.info("Listing files in dir {}".format(config.get("System","location_to_watch")))
        data_in_dir = os.listdir(config.get("System", "location_to_watch"))
        logging.debug(f"{data_in_dir}")

        for each in data_in_dir:
            if each == "GOOD":
                pass
            else:
                file_name, ext = each.split(".")
                logging.debug(f"getting filename: {filename}")

                try:
                    logging.debug(f"Trying to load wav file: {each}")
                    wav_file = AudioSegment.from_wav(each)
                    logging.info(f"Wav-file: [{each}] successfully loaded")
                except Exception as e:
                    logging.error("Wav_file could not be loaded.")
                    logging.error(e)
                
                try:
                    logging.debug(f"Trying to convert wav2mp3")
                    export_path ="{}/{}.{}".format(config.get("System", "location_to_write"), file_name, config.get("System", "convert_format"))
                    wav_file.export(export_path, format=config.get("System", "convert_format"))
                    logging.info(f"File: [{export_path}] was created successfully")
                except Exception as e:
                    logging.error("File could not be converted")
                    logging.error(e)
                
                try:
                    shutil.move(each, "./GOOD/")
                    logging.info(f"Moved {each} to GOOD folder")
                except Exception as e:
                    logging.error(f"Could not move {each} to good")
                    logging.error(e)
                


