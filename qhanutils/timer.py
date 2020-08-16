"""
    Timer - timing utility
    Written by Lin Liang-Han (qhan)
    Created at 2018.2.8
    Last update: 2019.7.25
"""

from __future__ import print_function
import numpy as np
import texttable as tt
import time


class TimeLabel():
    
    def __init__(self, name, hist_len=1000):
        self.name = name
        
        # last start timestamp
        self.start = None
        
        # min, max
        self.min = np.inf
        self.max = 0
        
        # history for avg
        self.hist = []
        self.hist_len = hist_len
        self.avg = None
        
    def update(self, t):
        # update min, max
        if t < self.min: 
            self.min = t
        if t > self.max:
            self.max = t
        
        # update history
        self.hist.append(t)
        if len(self.hist) > self.hist_len:
            self.hist.pop(0)
            
        # update average
        if len(self.hist) > 0:
            self.avg = np.mean(self.hist)


class Timer():
    
    def __init__(self, labels=[], unit='s'):
        self.labels = {name: self.create_label(name) for name in labels}
        
        # start time without label (anonymous)
        self.start = None
        
        # init unit
        self.units = {
            'us': 10 ** (-6),
            'ms': 10 ** (-3),
            's': 10 ** (0),
            'min': 60,
            'hr': 60 * 60,
            'day': 60 * 60 * 24
        }
        self.set_unit(unit)
        
    def tic(self, name=None):
        t = time.time()
        
        # if name specified
        if name:
            # label already created
            if name in self.labels:
                self.labels[name].start = t

            # label not created yet
            else:
                self.create_label(name)
                self.labels[name].start = t
            
        # start anonymous
        else:
            self.start = t
        
    def toc(self, name=None):
        t = time.time()
        
        try:
            # if name specified
            if name:
                period = t - self.labels[name].start
                self.labels[name].update(period)
            
            # end anonymous
            else:
                period = t - self.start
                
            return period / self.base

        except (TypeError, KeyError) as e:
            print('[Error] start time not set.')
        
        return None

    def create_label(self, name):
        if name not in self.labels:
            self.labels[name] = TimeLabel(name)
            
        else:
            print('[Error] label already existed.')

    def reset_label(self, name):
        if name in self.labels:
            self.labels[name].reset()
        
        else:
            print('[Error] label not exists.')

    def remove_label(self, name):
        if name in self.labels:
            self.labels.pop(name, None)
            
        else:
            print('[Error] label not exists.')
            
    def set_unit(self, unit):
        if unit in self.units:
            self.unit = unit
            self.base = self.units[unit]
        
        else:
            print('[Error] unit not exists:', unit)
            print('[Timer] unit set to second.')
            self.unit = 's'
            self.base = self.units[self.unit]
    
    def get_data(self):
        b = self.base
        data = []
        for name in self.labels:
            d = self.labels[name]
            data.append([name, d.max / b, d.min / b, d.avg / b])
            
        return data
    
    def summary(self):
        header = [['Name', 'Min', 'Max', 'Avg']]
        data = self.get_data()

        table = tt.Texttable()
        table.set_cols_align(['l', 'r', 'r', 'r'])
        table.set_cols_dtype(['t', 'f', 'f', 'f'])
        table.add_rows(header + data)
        
        print(table.draw() + '\n(%s)' % self.unit)
