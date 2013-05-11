import time
Filename = "log.txt"
class Logger():
     def __init__(self,filename):
        self.filename = filename
        self.open()

     def __del__(self):
        self.close()

     def open(self):
        self.handle = open(self.filename,"a")
        self.handle.write("--------------------------------------------------\n")
        self.handle.write(time.strftime("%d-%m-%y %H:%M:%S")+"\n")
        self.handle.write("**************************************************\n")

     def logme(self,text):
        self.handle.write(text)

     def close(self):
        self.handle.write("**************************************************\n")
        self.handle.write("\n")
        self.handle.close()

lg = Logger(Filename)

def log(text):
    log_to_stdout(text)

def log_to_stdout(text):
    print text,

def log_to_file(text):
    lg.logme(text)



