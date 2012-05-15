'''
Created on May 15, 2012

@author: david
'''

class ContextHistory(dict):
    '''
    classdocs
    '''


    def __str__(self):
        result = ""
        for key, value in self.iteritems():
            result += "%s -> %s\n" % (key, value)
        return result
        