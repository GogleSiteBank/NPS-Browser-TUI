import sys, os, requests, re, time; os.system("")

class ProgressBar:
    def __init__(self, total_size):
        self.total_size = total_size
        self.current_size = 0
        self.stime = time.time()
        self.bar_length = 30

    def update(self, size):
        self.current_size += size
        progress = self.current_size / self.total_size * 100
        self.print_progress(progress)

    def print_progress(self, progress):
        filled_length = int(self.bar_length * progress // 100)
        bar_str = '=' * filled_length + '-' * (self.bar_length - filled_length)
        print(f"\033[KProgress: [{bar_str}] {progress:.2f}% ({self.current_size/1048576:.2f}MB/{self.total_size/1048576:.2f}MB, {(time.time() - self.stime):.1f}s)", end='\r', flush=True) 


def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    progress_bar = ProgressBar(total_size)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                progress_bar.update(len(chunk))

if str(sys.argv[1])[::-1][:4] != "vst.":
    print("Incorrect Database file/Usage!\nUsage: python -u NPS_BTUI.py <.tsv DB URL>")
    sys.exit(1)

DB_Type = None
Console_Type = None

DB_Types = ["GAMES","DLCS","THEMES","UPDATES","DEMOS","AVATARS"]

DDLs = []
names = []

for _type in DB_Types:
    if _type in sys.argv[1]:
        print("Found DB Type! (%s)" % _type)
        DB_Type = _type

for console in ["PS3", "PSM", "PSX", "PSV", "PSP"]:
    if console in sys.argv[1]:
        print("Found Console Type! (%s)" % console)
        Console_Type = console

PS3 = [[0, 1, "PS3", 2, 3, 4, 6],[0, 1, "PS3", 2, 3, 4, 6],[0, 1, "PS3", 2, 3, 4, 6],[0, 1, "PS3", 2, 3, 4, 6],[0, 1, "PS3", 2, 3, 4, 6]]
PSM = [[0, 1, "PSM", 2, 3, 5, 6]]
PSX = [[0, 1, "PSX", 2, 3, 5, 7]]
PSV = [[0, 1, "PS-VITA", 2, 3, 6, 8],[0, 1, "PS-VITA", 2, 3, 5, 6],[0, 1, "PS-VITA", 2, 3, 5, 6],[0, 1, "PS-VITA", 2, 6, 7, 8] ]
PSP = [[0,1,2,3,4,6,9],[0,1, "DLC", 2, 3, 5, 8],[0,1, "THEME", 2, 3, 5, 8],[0, 1, "UPDATE", 2, 3,5, 8],[0,1,2,3,4,6,8]]


exec("Indexing = %s[DB_Types.index(DB_Type)]" % Console_Type)

with open(os.getenv("temp") + "\\nps_btuitemp", "wb+") as database:
    database.write(requests.get(sys.argv[1]).content)
    database.seek(0)
    for index, line in enumerate(database.readlines()):
        if index == 0: continue
        content = line.decode().split("\t")
        try:
            _gametype = content[Indexing[2]]
        except:
            _gametype = Indexing[2]
        try:
            size = round(int(content[Indexing[6]]) / 1048576, 2)
        except:
            size = "Couldn't be found"
        DDLs.append(content[Indexing[4]])
        names.append(content[Indexing[3]])
        print(f"\n{DB_Type.strip("S")} Number: {index}\n{DB_Type.strip("S")} Region Code: {content[Indexing[0]]}\n{DB_Type.strip("S")} Region: {content[Indexing[1]]}\n{DB_Type.strip("S")} Type: {_gametype}\nTitle: {content[Indexing[3]]}\n{DB_Type.strip("S")} DDL: {content[Indexing[4]]}\n{DB_Type.strip("S")} Modified Date: {content[Indexing[5]]}\n{DB_Type.strip("S")} Size: {size} MB\n")

filereadable = lambda s: re.sub(r'[^\w\s]', '', s.strip().replace('[', '').replace(']', ''))[:255]
getDDL = int(input("\nItem Number: "))
print("Downloading Item:\nDDL: %s\nName: %s\nFile Name: %s" % (DDLs[getDDL-1].strip(), names[getDDL-1], filereadable(names[getDDL-1]) + ".pkg"))

url = DDLs[getDDL-1].strip()
stime = time.time()
download_file(url, filereadable(names[getDDL-1]) + ".pkg")
print(f"\nDownload Finished in {(time.time() - stime) * 1000:.2f}ms!")
