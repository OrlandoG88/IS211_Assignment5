import argparse
from urllib.request import urlopen
import csv
import re
import time


class Queue():
#makes a queue in list usinf FIFO; right is the front of the list and left is the back of the list
    def __init__(self):
        self.items = []

    def items(self):
        return self.items

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server():
#sever class to record waiting times in Queue
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0
#Lowers time in timer per request and sets to server to available
    def tick(self):
        if self.current_request != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_request = None
#checks for pending requests
    def busy(self):
        if self.current_request != None:
            return True
        else:
            return False
#starts next server request
    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.get_processing_time()


class Request():
    def __init__(self, time, processing_time):
        self.timestamp = time  # time request was created and placed in queue
        self.processing_time = processing_time  # index row[2] from csv_reader which is time it takes to proccess requests

    def get_stamp(self):
        return self.timestamp

    def get_processing_time(self):
        return self.processing_time

    def wait_time(self, current_time):
        if current_time - self.timestamp <= 0:
            # print(self.processing_time)
            return self.processing_time
        else:
            return current_time - self.timestamp  # amt of time spent in queue before request was processed
            # print(current_time - self.timestamp)


def simulateOneServer(file):
    web_server = Server()
    request_queue = Queue()
    waiting_times = []

    csv_file = urlopen(file)
    csv_list = [i.decode("utf-8")for i in csv_file]  # decode csv and store each row as a string in a big list
    csv_reader = csv.reader(csv_list,delimiter=',')  # take each row (single string) and and break each string into separate elements of a smaller list
    requests = [[int(row[0]), row[1], int(row[2])] # unpacks list and converts row[0] and row[2] from csv to ints
    for row in csv_reader]

    for current_second in range(len(requests)):
#process Queue by length of incoming request and time for processing
        request = Request(requests[current_second][0], requests[current_second][2])
        request_queue.enqueue(request)
#adds requests to Queue
        if (not web_server.busy()) and (not request_queue.is_empty()):
#checks to see if server is busy and pending requests in queue
            next_request = request_queue.dequeue()
            waiting_times.append(next_request.wait_time(current_second))
            web_server.start_next(next_request)

        web_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average wait %6.2f secs. %i requests remaining." % (average_wait, request_queue.size()))

def main(file):
    simulateOneServer(file)




if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    file = args.file
    main(file)




