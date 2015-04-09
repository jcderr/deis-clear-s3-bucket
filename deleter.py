#!/usr/bin/env python

import time
import boto
from boto.exception import BotoServerError
from Queue import Queue
from threading import Thread
import os
import sys

bucket_name = os.getenv('BUCKET', None)

if not bucket_name:
    print "No bucket given. Fail!"
    sys.exit(-1)

workers = int(os.getenv('WORKERS', 2))
build_cooldown = float(os.getenv('BUILD_COOLDOWN', 0.25))
delete_cooldown = float(os.getenv('DELETE_COOLDOWN', 0.25))
initial_wait = int(os.getenv('INITIAL_WAIT', 5))

print '''
#################################
### Massive S3 Bucket Clearer ###
### F: 1/{} ## W: {}/{} ######
'''.format(build_cooldown, workers, delete_cooldown)

s3 = boto.connect_s3()
bucket = s3.get_bucket(bucket_name)

keypool = Queue()

def build_keypool(bucket, q, cooldown):
    counter = 0
    _file_list = []
    try:
        for k in bucket.list():
            if counter >= 1000:
                time.sleep(cooldown)
                counter = 0
                q.put(_file_list)
                _file_list = []
            _file_list.append(k.name)
            counter = counter + 1
    except BotoServerError, e:
        print "Throttle requested."
        time.sleep(cooldown * 10)

def consume_keypool(bucket, q, cooldown):
    counter = 0
    while True:
        if counter >= 1000:
            time.sleep(cooldown)
            counter = 0
        _list = q.get()
        print 'deleting {}:{}'.format(_list[0], _list[1])
        try:
            bucket.delete_keys(_list)
        except BotoServerError, e:
            print 'Delete throttle requested.'
            time.sleep(cooldown * 100)
        q.task_done()
        counter = counter + 1

print 'Filling the keypool'
filler = Thread(target=build_keypool, args=(bucket, keypool, build_cooldown))
filler.start()
time.sleep(initial_wait)

for i in range(workers):
    print "Starting worker #{}".format(i)
    worker = Thread(target=consume_keypool, args=(bucket, keypool, delete_cooldown))
    worker.start()

print "Working..."
filler.join()
print "Done."
