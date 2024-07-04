import os
import time
import shutil
import subprocess
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Watcher:
    def __init__(self, directory_to_watch, image_dir, document_dir):
        self.directory_to_watch = directory_to_watch
        self.image_dir = image_dir
        self.document_dir = document_dir
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.image_dir, self.document_dir)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            logging.info("Observer stopped")
        except Exception as e:
            self.observer.stop()
            logging.error(f"Error: {e}")
        finally:
            self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, image_dir, document_dir):
        self.image_dir = image_dir
        self.document_dir = document_dir
        self.processed_files = set()

    @staticmethod
    def is_temporary_file(file):
        return file.lower().endswith('.tpm') or file.lower().endswith('.crdownload')

    @staticmethod
    def is_file_stable(file, check_duration=1, check_interval=0.1):
        """Check if the file size remains stable over a period of time."""
        initial_size = os.path.getsize(file)
        time.sleep(check_duration)
        new_size = os.path.getsize(file)
        return initial_size == new_size

    def process(self, event):
        if event.is_directory:
            return

        if event.event_type in ('created', 'modified', 'moved'):
            file = event.src_path
            if self.is_temporary_file(file) or file in self.processed_files:
                return

            filename = os.path.basename(file)
            logging.info(f"Received event {event.event_type} - {file}")

            destination = None
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.gif')):
                destination = self.image_dir
            elif file.lower().endswith(('.pdf', '.txt', '.doc', '.docx', '.docm', '.xml', '.csv', '.xlsx', '.xlsm',
                                        '.xls', '.pptx', '.ppt')):
                destination = self.document_dir

            if destination:
                retries = 5
                delay = 1  # seconds
                for i in range(retries):
                    if os.path.exists(file) and self.is_file_stable(file):
                        try:
                            shutil.move(file, destination)
                            self.processed_files.add(file)
                            file_new_path = os.path.join(destination, filename)
                            subprocess.Popen(r'explorer /select, "%s"' % file_new_path)
                            logging.info(f"Moved {filename} to {destination}")
                            break
                        except (shutil.Error, FileNotFoundError) as e:
                            logging.error(f"Error moving file {filename}: {e}")
                            time.sleep(delay)
                        except Exception as e:
                            logging.error(f"Unexpected error: {e}")
                    else:
                        logging.info(f"File {filename} is not yet stable. Retrying...")
                        time.sleep(delay)

    def on_any_event(self, event):
        self.process(event)


if __name__ == "__main__":
    user_home = os.path.expanduser('~')
    downloads_dir = os.path.join(user_home, 'Downloads')
    images_dir = os.path.join(user_home, 'Imagens')
    documents_dir = os.path.join(user_home, 'Documentos')

    w = Watcher(downloads_dir, images_dir, documents_dir)
    w.run()
