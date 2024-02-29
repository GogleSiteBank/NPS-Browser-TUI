import sys, os, requests, re
from tqdm import tqdm

if str(sys.argv[1])[::-1][:4] != "vst.":
    print("Incorrect Database file/Usage!\nUsage: python -u NPS_BTUI.py <.tsv DB URL>")
    sys.exit(1)

DB_Type = None
Console_Type = None

DB_Types = [
    "GAMES",
    "DLCS",
    "THEMES",
    "UPDATES",
    "DEMOS",
    "AVATARS"
]

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

PS3 = [
    [0, 1, "PS3", 2, 3, 4, 6],
    [0, 1, "PS3", 2, 3, 4, 6],
    [0, 1, "PS3", 2, 3, 4, 6],
    [0, 1, "PS3", 2, 3, 4, 6],
    [0, 1, "PS3", 2, 3, 4, 6]
]

PSM = [
    [0, 1, "PSM", 2, 3, 5, 6]
]

PSX = [
    [0, 1, "PSX", 2, 3, 5, 7]
]

PSV = [
    [0, 1, "PS-VITA", 2, 3, 6, 8],
    [0, 1, "PS-VITA", 2, 3, 5, 6],
    [0, 1, "PS-VITA", 2, 3, 5, 6],
    [0, 1, "PS-VITA", 2, 6, 7, 8] 
]

PSP = [
    [0,1,2,3,4,6,9],
    [0,1, "DLC", 2, 3, 5, 8],
    [0,1, "THEME", 2, 3, 5, 8] ,
    [0, 1, "UPDATE", 2, 3,5, 8],
    [0,1,2,3,4,6,8]
]


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
        print(f"\n{DB_Type.strip("S")} Number: {index + 1}\n{DB_Type.strip("S")} Region Code: {content[Indexing[0]]}\n{DB_Type.strip("S")} Region: {content[Indexing[1]]}\n{DB_Type.strip("S")} Type: {_gametype}\nTitle: {content[Indexing[3]]}\n{DB_Type.strip("S")} DDL: {content[Indexing[4]]}\n{DB_Type.strip("S")} Modified Date: {content[Indexing[5]]}\n{DB_Type.strip("S")} Size: {size} MB\n")

filereadable = lambda s: re.sub(r'[^\w\s]', '', s.strip().replace('[', '').replace(']', ''))[:255]
try:
    getDDL = int(input("\nItem Number: "))
    print("Downloading Item:\nDDL: %s\nName: %s\nFile Name: %s" % (DDLs[getDDL-1].strip(), names[getDDL-1], filereadable(names[getDDL-1]) + ".pkg"))

    url = DDLs[getDDL-1].strip()
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(filereadable(names[getDDL-1]) + ".pkg", 'wb') as file, tqdm(
        desc="Downloading",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            progress_bar.update(len(data))

except ValueError:
    print("ValueError - Incorrect Number")
except IndexError:
    print("Incorrect number value")
