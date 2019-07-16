# $this.py EXTRACTED_PAK_FILES REGEX OUTPUT_DIR
import sys, os, re, subprocess

basePath = sys.argv[1]
file_test = re.compile(sys.argv[2])

print("Search path:", basePath)
print("Regex:", sys.argv[2])

class ERunResultType:
    PENDING = object()
    SUCCESS = object()
    FAIL = object()

class SAssetFileData:
    def __init__(self, path, filename):
        self.result = ERunResultType.PENDING
        self.dirpath = path
        self.filename = filename
        self.clean_filename = filename.replace(".uasset", "")
        self.clean_path = os.sep.join([self.dirpath, self.clean_filename])

uassets = {}

print("Scanning for assets")
for (dirpath, dirnames, filenames) in os.walk(basePath):
    for filename in filenames:
        if file_test.match(filename):
            uassets[os.sep.join([dirpath, filename])] = SAssetFileData(dirpath, filename)

amount = len(uassets.keys())
print("Found", amount, "applicable items.")

print("Extracting data from detected assets")
current = 0
amount_str_length = len(str(amount))
for uasset_path in uassets:
    uasset_info = uassets[uasset_path]
    current = current + 1
    uasset_name = uasset_info.filename
    print("[", str(current).rjust(amount_str_length), " / ", amount, "] ",
          uasset_name.ljust(50),
          sep="", end="")
    
    process = subprocess.Popen(['./extractor', "serialize", uasset_info.clean_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    code = process.wait()
    json_path = uasset_info.clean_path + ".json"
    if os.path.exists(json_path):
        print("+")
        uassets[uasset_path].result = ERunResultType.SUCCESS
        final_dir = sys.argv[3] + "/" + uasset_info.dirpath.replace(basePath, "")
        final_json_path = final_dir + "/" + uasset_name + ".json"
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)
        os.rename(json_path, final_json_path)
        subprocess.Popen(['python', './json-cleanup.py', final_json_path, final_json_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("-")
        uassets[uasset_path].result = ERunResultType.FAIL

results = uassets.values()
print(len(results), "tasks finished -",
      sum(value.result == ERunResultType.SUCCESS for value in results),
      "succeded, ",
      sum(value.result == ERunResultType.FAIL for value in results),
      "failed.")