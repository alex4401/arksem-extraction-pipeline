import os

class Asset:
    def __init__(self, path, filename, tag):
        filename_without_extension = '.'.join(filename.split('.')[:-1])
        uexp_filename = os.sep.join([path, filename_without_extension + '.uexp'])

        self.tag = tag
        self.name = filename_without_extension
        self.uexp_file = uexp_filename if os.path.exists(uexp_filename) else None
        self.directory = path
        self.path = os.sep.join([path, filename])
    
    def __str__(self):
        return f"Asset({self.tag}, {self.name})"

    @classmethod
    def make(self, descriptor, data = None):
        if data is None:
            raise Exception('No tag specified.')
        
        path, filename = descriptor
        return Asset(path, filename, data)
