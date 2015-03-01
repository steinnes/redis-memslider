#!/usr/bin/env python
# encoding: utf-8
""" slider.py - Gradually lower redis maxmemory.  """

import redis
import time
import argparse

class TimeIt(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self, *args, **kwargs):
        self.start_t = time.time()

    def __exit__(self, *args, **kwargs):
        self.end_t = time.time()
        print "{}: took {}s".format(self.name, self.end_t - self.start_t)


class MemorySlider(object):
    def __init__(self, redis_client, reduction, steps, interval):
        self.redis = redis_client
        self.steps = steps
        self.reduction = int(reduction)
        self.current_maxmemory = int(self.redis.config_get('maxmemory')['maxmemory'])
        self.initial_maxmemory = self.current_maxmemory
        self.target_maxmemory = self.initial_maxmemory - self.reduction
        self.interval = interval

        if self.current_maxmemory == 0:
            raise Exception("No maxmemory setting in redis currently, please set one before attempting to reduce.")

        if self.target_maxmemory >= self.current_maxmemory:
            raise Exception("Target memory: {} is >= current maxmemory {}".format(
                self.target_maxmemory, self.current_maxmemory))

        self.diff = (self.current_maxmemory - self.target_maxmemory) / self.steps

    def confirm(self):
        response = raw_input("About to reduce maxmemory from {} -> {} in {} steps of {}, with {}s intervals, continue? [Y/n]".format(
            self.initial_maxmemory, self.target_maxmemory, self.steps, self.diff, self.interval))
        if response.strip().lower() in ('y', ''):
            return True
        return False

    def start(self):
        while self.current_maxmemory > self.target_maxmemory:
            new_maxmemory = self.current_maxmemory - self.diff
            with TimeIt("Setting maxmemory to {}".format(new_maxmemory)):
                self.redis.config_set('maxmemory', new_maxmemory)

            self.current_maxmemory = new_maxmemory
            time.sleep(self.interval)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--host', default='localhost', required=False)
    parser.add_argument('-p', '--port', type=int, default=6379, required=False)
    parser.add_argument('-r', '--reduction', type=int, required=True, help='`maxmemory` reduction in bytes')
    parser.add_argument('-s', '--steps', type=int, default=100, required=False, help='In how many steps do you want to reduce, default 100')
    parser.add_argument('-i', '--interval', type=int, default=30, required=False, help='How long to sleep between steps, default 30s')
    
    args = parser.parse_args()
    r = redis.Redis(args.host, args.port)
    memory_slider = MemorySlider(r, args.reduction, args.steps, args.interval)
    if memory_slider.confirm():
        memory_slider.start()


if __name__ == "__main__":
    main()
