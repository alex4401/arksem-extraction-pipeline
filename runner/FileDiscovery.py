import os
import re
import time
import subprocess

class DiscoveryResult:
    def __init__(self):
        self.__objects__ = []
        self.__entries__ = []
    
    def add_entry(self, path, file):
        self.__entries__.append((path, file))
    
    def get_entries(self, selector):
        result = []
        print('Finding entries that match', selector)
        pattern = re.compile(selector)
        for entry in self.__entries__:
            if type(entry) is tuple:
                if pattern.match(entry[1]):
                    result.append(entry)
        return result

    def __len__(self):
        return len(self.__entries__)
    
    def cast_as(self, type_cls, data=None, selector="^(.*)$"):
        entries = self.get_entries(selector)
        print("Casting", len(entries), "entries to", type_cls.__name__)

        for entry in entries:
            self.__objects__.append(type_cls.make(entry, data))
        
        return self
    
    def filter(self, test):
        objects = self.__objects__
        self.__objects__ = []

        for entry in objects:
            if test(entry):
                self.__objects__.append(entry)
        
        print('Applied a filter and left', len(self.__objects__), 'entries out of', len(objects))
        return self
    
    def run_process_for_each(self, generator, max_simultaneous = 1):
        processes = []
        def _wait_for_all(processes):
            for process in processes:
                process.wait()

        print('Running a process for every entry')
        start_time = time.time()
        for entry in self.__objects__:
            # Wait for subprocess to end, then clean the array.
            if len(processes) >= max_simultaneous:
                _wait_for_all(processes)
                processes = []
            # Start a subprocess
            command = generator(entry)
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            processes.append(process)

        print('Ensuring the subprocesses have ended their work')
        _wait_for_all(processes)
        end_time = time.time()
        duration = end_time - start_time
        print('All processes have finished their work. Execution took', "{0:.3f}".format(duration), 'seconds.')
        return self
    
    def print_all(self):
        print('Printing', len(self.__objects__), 'objects')
        for entry in self.__objects__:
            print(entry)
        
        return self

def discover(patterns, basepath="."):
    print('Compiling patterns')
    if type(patterns) is str:
        patterns = [patterns]
    __compiled_patterns__ = []
    for pattern in patterns:
        __compiled_patterns__.append(re.compile(pattern))

    result = DiscoveryResult()
    print('Discovering files for pattern', pattern, 'in', basepath)

    scannedCount = 0
    for (dirpath, dirnames, filenames) in os.walk(basepath):
        for filename in filenames:
            scannedCount = scannedCount + 1
            for pattern in __compiled_patterns__:
                if pattern.match(filename):
                    result.add_entry(dirpath, filename)
                    continue

    print('Scanned', scannedCount, 'files and marked', len(result), 'files.')
    return result