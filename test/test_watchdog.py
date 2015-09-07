# -*- coding: utf-8 -*-
import sys, os
import time
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

def execute(cmd) :
    fd = subprocess.Popen(cmd, shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    fd.wait()
    return fd.stdout, fd.stderr
 
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)
        if what == 'file':
            #State Service
            for x in ['172.31.7.217', '172.31.7.218', '172.31.7.216']:
                cmd = "scp -P 10022 -i /home/ec2-user/key/osc-aws-key.pem -r %s ec2-user@%s:%s" % (event.src_path, x, event.src_path)
                std_out, std_err = execute(cmd)
                #print pid
                for line in std_err.readlines() :
                    if "No such file or directory" in line:
                        cmd = "ssh -p 10022 -i /home/ec2-user/key/osc-aws-key.pem ec2-user@%s \"mkdir -p %s\"" % (x, os.path.dirname(event.src_path))
                        std_out, std_err = execute(cmd)
                        cmd = "scp -P 10022 -i /home/ec2-user/key/osc-aws-key.pem -r %s ec2-user@%s:%s" % (event.src_path, x, event.src_path)
                        std_out, std_err = execute(cmd)

                        
            

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler() #LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()