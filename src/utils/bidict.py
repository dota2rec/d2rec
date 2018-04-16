import sys

class bdict(dict):
    def __init__(self, *args, **kwargs):
        super(bdict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.iteritems():
            if value in self.inverse:
                raise Exception("bdict non-unique value error")
            else:
                self.inverse[value] = key

    def __setitem__(self, key, value):
        if key in self:
            # remove previous val-key pair in inverse
            del self.inverse[self[key]]
            
        if value in self.inverse:
            raise Exception("bdict non-unique value error")
        else:
            super(bdict, self).__setitem__(key, value)
            self.inverse[value] = key  

    def __delitem__(self, key):
        del self.inverse[self[key]]
        super(bdict, self).__delitem__(key)
    
    def __print__(self):
        sys.stdout.write('dictionary: {')
        for key in self:
            sys.stdout.write(str(key) + ':' + str(self[key]) + ',')
        sys.stdout.write('\b}')
        
        sys.stdout.write('\ninverse dictionary: {')
        for key in self.inverse:
            sys.stdout.write(str(key) + ':' + str(self.inverse[key]) + ',')
        sys.stdout.write('\b}\n')
        sys.stdout.flush()

    def __len__(self):
        return len(self)