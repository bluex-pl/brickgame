#!/usr/bin/env python
"""
data_make is a module packing data used by BrickGame
"""

import cPickle
from default_config import config

__all__ = ('pack', 'load')

err = 'Error while {0} configuration file:'

def pack(data=config, file_name='new_config.dat'):
    f = open(file_name, 'wb')
    cPickle.dump(data, f, -1)
    del f

def load(file_name=None):
    try:
        f = open(('config.dat' if file_name is None else file_name), 'rb')
        data = cPickle.load(f)
        del f
        for k, v in data.iteritems():
            if config.has_key(k):
                    config[k].update(v)
            else:
                config[k] = v
    except IOError, detail:
        if file_name is not None:
            print err.format('loading'), detail
    except TypeError, detail:
        print err.format('processing'), detail
    return config
