import threading
from helper import Helper


class Main:
    def __init__(self) -> None:
        pass


    def run(number_threads: int, stream_link: str, window_size: tuple = (300, 500)):
        helper = Helper()
        threads = []
        for x, y in helper.setPositionChrome(*window_size, number_threads):
            
            driver = helper.create_driver(window_size=window_size, position=(x, y))
            
            thread = threading.Thread(target=helper.watch_live, args=(driver, stream_link))
            thread.start()
            threads.append(thread)

        
        for thread in threads:
            thread.join()



if __name__ == '__main__':
    Main.run(10, 'https://www.youtube.com/watch?v=3UR2V67PddQ')