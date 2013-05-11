#!/usr/bin/python

import Queue
import threading
import time
import argparse
import database
import webwork
#from logging import log_to_file as log
from logging import log

Slow = False
#Slow = True
exitFlag = 0

class Manager(threading.Thread):
    def __init__(self,batch_size):
        threading.Thread.__init__(self)
        self.batch_size = batch_size
        

    def run(self):
        log("Manager Initialised\n")
        self.batch_query()
        log("Manager Fired\n")

    def batch_query(self):
        while not exitFlag:
            finalQLock.acquire()
            if not finalQ.empty():
                slaveryLock.acquire()
                slaveryQ.put("Manager")
                self.querylist=[]
                for x in xrange(min(finalQ.qsize(),self.batch_size)):
                    self.querylist.append(finalQ.get())
                finalQLock.release()
                slaveryLock.release()
                res = self.send_query()
                self.put_back(res)
                slaveryLock.acquire()
                slaveryQ.get()
                slaveryLock.release()
            else:
                finalQLock.release()
            if Slow:
                time.sleep(1)

    def send_query(self):
        log("Manager Pulled out from finalQ :"+repr(self.querylist)+"\n")
        log("Manager sending Query :" +repr(self.querylist)+"\n")
        res=database.query(self.querylist)
        log("DB Result : "+repr(res)+"\n")
        return res


    def put_back(self,res):
        rawQLock.acquire()
        for individual in res:
            rawQ.put(individual)
        rawQLock.release()
        log("Manager Feeding it into rawQ :" +repr(res)+"\n")



class Slaves (threading.Thread):

    def __init__(self, slaveID,max_depth):
        threading.Thread.__init__(self)
        self.slaveID = slaveID
        self.max_depth = max_depth

    def run(self):
        log("Birth of Slave " + str(self.slaveID)+"\n")
        self.extract_data()
        log("Death of Slave " + str(self.slaveID)+"\n")

    def hard_work(self,data):
        self.datalist = webwork.process(data)


    def extract_data(self):
        while not exitFlag:
            rawQLock.acquire()
            if not rawQ.empty():
                slaveryLock.acquire()
                data = rawQ.get()
                slaveryQ.put(self.slaveID)
                slaveryLock.release()
                rawQLock.release()
                log("Slave %s Pulling out from rawQ -> %s\n" % (self.slaveID, data))
                self.hard_work(data)
                self.fill_data()
            else:
                rawQLock.release()
            if Slow:
                time.sleep(1)

    def fill_data(self):
        self.discard()
        log("Slave %s Pushing into finalQ -> %s\n" % (self.slaveID, repr(self.datalist)))
        finalQLock.acquire()
        slaveryLock.acquire()
        slaveryQ.get()
        for data in self.datalist:
            finalQ.put(data)
        finalQLock.release()
        slaveryLock.release()

    def discard(self):
        self.datalist = [(u,d) for u,d in self.datalist  if d < self.max_depth]



def shellParse():
    parser = argparse.ArgumentParser(description='A Multi-threaded and extensible Web Crawler')
    parser.add_argument('-u','--urls', help='The Urls of websites to crawl', required=True,default='http://www.google.com')
    parser.add_argument('-d','--depth', help='The Depth to crawl (default:5),',default=4)
    parser.add_argument('-t','--threads', help='The Slave population on this system (default:3),',default=3)
    parser.add_argument('-b','--batch', help='The Batch Length of Database Query (default:10),',default=10)
    args = vars(parser.parse_args())
    return args



if __name__ == '__main__':
    c_args =  shellParse()

    max_depth = 4
    population = 3
    batch_size = 10
    urlList = [("http://www.google.com",0)]

    max_depth = c_args["depth"]
    population = c_args["threads"]
    batch_size = c_args["batch"]
    urlList = map(lambda x:(x,0),c_args["urls"].split())

    rawQLock = threading.Lock()
    finalQLock = threading.Lock()
    slaveryLock = threading.Lock()
    rawQ = Queue.Queue(10)
    finalQ = Queue.Queue()
    slaveryQ = Queue.Queue()
    slave_cluster = []
#init database
    database.init()


# Create Manager thread
    manager = Manager(batch_size)
    manager.start()
# Create new Slave threads -> each having a Slave Id
    for i in xrange(1,population+1):
        slave = Slaves(i,max_depth)
        slave.start()
        slave_cluster.append(slave)

# Fill the queue
    #rawQLock.acquire()
    #for url in urlList:
    #    rawQ.put(url)
    #rawQLock.release()

    finalQLock.acquire()
    for url in urlList:
        finalQ.put(url)
    finalQLock.release()


# Notify the Slave and Manager threads if its time to exit
    while True:
        rawQLock.acquire()
        finalQLock.acquire()
        slaveryLock.acquire()
        if  rawQ.empty() and finalQ.empty() and slaveryQ.empty() :
            exitFlag = 1
            rawQLock.release()
            finalQLock.release()
            slaveryLock.release()
            break
        rawQLock.release()
        finalQLock.release()
        slaveryLock.release()

# Wait for all threads to complete
    for slave in slave_cluster:
        slave.join()
    manager.join()
    log("Exiting Main Thread\n")
