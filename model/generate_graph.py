import geopandas as gpd
import json,math

print("importing shapefile ",end="")
file_path = "data/L4_1_BDOT10k__OT_SKJZ_L.shp"
gdf = gpd.read_file(file_path)
print("DONE")

node_ids = [] # str(idIIP_BT_I+"_"+klasaDrogi+"_"+node_id)
node_pes = [] # [x,y] coordinate in epsg2180 (1 decimal place precision)

print("parsing gdf ",end="")
# extract points from shapefile
for index,row in gdf.iterrows():
    for index,point in enumerate(row["geometry"].coords):
        if index!=0 and index!=len(row["geometry"].coords)-1: continue # comment this line to get a high precision graph (linestring exploded into points)
        node_ids.append(row["idIIP_BT_I"]+"_"+row["klasaDrogi"]+"_"+str(index))
        node_pes.append([round(point[0],1),round(point[1],1)])
print("DONE")

# addidional geometry data from geojson
print("importing geojson ",end="")
node_pws = [[] for i in range(len(node_pes))] # [x,y] coordinate in wgs84 (6 decimal places precision)
geofile = open("data/L4_1_BDOT10k__OT_SKJZ_L.geojson")
geojson = json.loads(geofile.read())
print("DONE")

# extract points from geojson
print("parsing geojson ",end="")
for index,row in enumerate(geojson["features"]):
    linestringID = row["properties"]["idIIP_BT_I"]
    linestringKD = row["properties"]["klasaDrogi"]
    for index,point in enumerate(row["geometry"]["coordinates"][0]):
        if index!=0 and index!=len(row["geometry"]["coordinates"][0])-1: continue # comment this line to get a high precision graph (linestring exploded into points)
        pointer = node_ids.index(linestringID+"_"+linestringKD+"_"+str(index))
        node_pws[pointer] = [round(point[0],6),round(point[1],6)]
print("DONE")

print("finding edges ",end="")
# generate edges between points
edges_raw = [] # [node_id1, node_id2, length]
for i in range(0,len(node_ids)-1):
    linestringid1 = node_ids[i].split("_")[0]
    linestringid2 = node_ids[i+1].split("_")[0]
    if linestringid1 != linestringid2: continue
    # index1 = int(node_ids[i].split("_")[2])
    # index2 = int(node_ids[i+1].split("_")[2])
    # if abs(index1-index2)!=1: continue
    length = math.sqrt(pow(node_pes[i][0]-node_pes[i+1][0],2)+pow(node_pes[i][1]-node_pes[i+1][1],2))
    edges_raw.append([node_ids[i],node_ids[i+1],length])
print("DONE")

print("fixing geometries ",end="")
# merge ducked up geometries
for i in range(0,len(node_pes)-1):
    for j in range(i+1,len(node_pes)):
        if node_pes[j]==node_pes[i]: # check if coordinates match
            for x in range(0,len(edges_raw)): # replace all point occurencies
                if edges_raw[x][0]==node_ids[j]: edges_raw[x][0]=node_ids[i]
                if edges_raw[x][1]==node_ids[j]: edges_raw[x][1]=node_ids[i]
print("DONE")

# remove unused nodes from 'rnodes'
print("removing unused nodes ",end="")
used_nodes=set()
for edge in edges_raw:
    used_nodes.add(edge[0])
    used_nodes.add(edge[1])
unused_nodes=[]
for i in range(0,len(node_ids)):
    if node_ids[i] in used_nodes: continue
    unused_nodes.append(i)
unused_nodes.sort(reverse=True)
for un in unused_nodes:
    node_ids.pop(un)
    node_pes.pop(un)
    node_pws.pop(un)
print("DONE")

print("saving nodes ",end="")
with open("rnodes","w+") as file:
    for i in range(0,len(node_ids)):
        file.write(str(i)+","+str(node_pws[i][0])+","+str(node_pws[i][1])+"\n")
print("DONE")

print("saving edges ",end="")
with open("redges","w+") as file:
    for i in range(0,len(edges_raw)):
        node_id1 = node_ids.index(edges_raw[i][0])
        node_id2 = node_ids.index(edges_raw[i][1])
        dlugoscDrogi = edges_raw[i][2]
        rclass = edges_raw[i][0].split("_")[1]
        speed_limit = 140
        if rclass == "S":  # ekspresowa
            speed_limit = 130
        elif rclass == "GP":  # główna ruchu przyspieszonego
            speed_limit = 110
        elif rclass == "G":  # główna
            speed_limit = 100
        elif rclass == "Z":  # zbiorcza
            speed_limit = 80
        elif rclass == "L":  # lokalna
            speed_limit = 60
        elif rclass == "D":  # zbiorcza
            speed_limit = 30
        czasDrogi = dlugoscDrogi/speed_limit
        file.write(str(node_id1)+","+str(node_id2)+","+str(dlugoscDrogi)+","+str(czasDrogi)+"\n")
print("DONE")