import time
import threading


class Scheduler:

    def __init__(self, callback, interval=300):
        self.callback = callback
        self.interval = interval
        self.running = False

    def start(self):

        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        thread.start()

    def stop(self):
        self.running = False

    def run(self):

        while self.running:

            try:
                self.callback()

            except Exception as e:
                print("Scheduler Error:", e)

            time.sleep(self.interval)