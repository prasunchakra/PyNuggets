# -------------------------------------------------------------
# # Project #5
# Project5.py
# -------------------------------------------------------------
import sys, os, threading, time, logging

EMPTY = -1

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

LOCAL = threading.local()


# -------------------------------------------------------------
def LOG(message):
    # -------------------------------------------------------------
    logging.debug(message)


#   print(message)

# -------------------------------------------------------------
class PRODUCER(threading.Thread):
    # -------------------------------------------------------------
    def __init__(self, threadID, threadName, count):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.item = threadID * 100
        self.count = count
        LOG(self.threadName + " created")

    def run(self):
        global threadLock, S, buffer, bufferIn, bufferOut, bufferCount

        while (self.count > 0):
            threadLock.acquire()
            if (bufferCount < S):
                buffer[bufferIn] = self.item
                bufferIn = (bufferIn + 1) % S
                bufferCount += 1
                LOG(self.threadName + " " + str(self.item))
                threadLock.release()
                self.item += 1
                self.count -= 1
            else:
                LOG(self.threadName + " waiting")
                threadLock.release()
                time.sleep(1)

        LOG(self.threadName + " terminated, produeced " + str(self.count))


# -------------------------------------------------------------
class CONSUMER(threading.Thread):
    # -------------------------------------------------------------
    STOP = False

    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.count = 0
        LOG(self.threadName + " created")

    def run(self):
        global threadLock, S, buffer, bufferIn, bufferOut, bufferCount

        while (not CONSUMER.STOP):
            threadLock.acquire()
            if (bufferCount > 0):
                LOCAL.item = buffer[bufferOut]
                bufferOut = (bufferOut + 1) % S
                bufferCount -= 1
                LOG(self.threadName + " " + str(LOCAL.item))
                threadLock.release()
                self.count += 1
            else:
                LOG(self.threadName + " waiting")
                threadLock.release()
                time.sleep(1)

        LOG(self.threadName + " terminated, consumed " + str(self.count))

    def StopConsumers():
        CONSUMER.STOP = True


# -------------------------------------------------------------
# main
# -------------------------------------------------------------
print("main thread name is ", threading.current_thread())

P = int(input("P? "))
C = int(input("C? "))
S = int(input("S? "))

# initialize buffer with S EMPTYs
buffer = []
for item in range(0, S):
    buffer.append(EMPTY)
bufferIn = 0;
bufferOut = 0;
bufferCount = 0

threadLock = threading.Lock()

# start PRODUCERs
producers = ["IGNORE"]
for i in range(1, P + 1):
    producers.append(PRODUCER(i, "Producer#" + str(i), 2 * S))
    producers[i].start()

# start CONSUMERs
consumers = ["IGNORE"]
for i in range(1, C + 1):
    consumers.append(CONSUMER(i, "Consumer#" + str(i)))
    consumers[i].start()

# wait for *ALL* PRODUCERs to terminate
LOG("main waiting on PRODUCERs")
for i in range(1, P + 1):
    producers[i].join()
LOG("main wait on PRODUCERs completed")

# wait for all produced items to be consumed
LOG("main waiting on CONSUMERs")
while (bufferCount != 0):
    time.sleep(1)

# "tell" CONSUMERs to stop running
CONSUMER.StopConsumers()

# wait for *ALL* CONSUMERs to terminate
for i in range(1, C + 1):
    consumers[i].join()
LOG("main wait on CONSUMERs completed")

LOG("main terminated")

sys.exit(0)
