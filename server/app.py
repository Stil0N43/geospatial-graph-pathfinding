from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json,csv,math

from classes.edge import Edge
from classes.graph import Graph
from classes.node import Node
from algorithms.a_star import a_star
from algorithms.dijkstra import dijkstra

nodes = []
graph = Graph()
with open("../model/rnodes",newline="\n") as csvfile:
    nodesreader = csv.reader(csvfile,delimiter=",",quoting=csv.QUOTE_NONNUMERIC)
    for row in nodesreader:
        nodes.append(row)
        Node(graph,row[1],row[2])
with open("../model/redges",newline="\n") as csvfile: # 8805-8808 [most zachodni]
    edgesreader = csv.reader(csvfile,delimiter=",",quoting=csv.QUOTE_NONNUMERIC)
    for row in edgesreader:
        # most zachodni przejezdny jedynie z polnocy na poludnie
        if row[0]==8808 and row[1]==8805: Edge(graph,int(row[0]),int(row[1]),row[2],row[3],True)
        else: Edge(graph,int(row[0]),int(row[1]),row[2],row[3])

class RequestBody(BaseModel):
    lat0:float
    lon0:float
    lat1:float
    lon1:float

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test_line/")
async def post_line(rb:RequestBody):
    return {"type":"FeatureCollection","features":[
        {"type":"Feature","geometry":{"type":"LineString","coordinates":[[rb.lon0,rb.lat0],[rb.lon1,rb.lat1]]}}
    ]}

@app.post("/test_point/")
async def post_point(rb:RequestBody):
    mindiff0=180
    mindiff1=180
    closest0=0
    closest1=0
    for node in nodes:
        newdiff0=math.sqrt(pow(node[1]-rb.lon0,2)+pow(node[2]-rb.lat0,2))
        newdiff1=math.sqrt(pow(node[1]-rb.lon1,2)+pow(node[2]-rb.lat1,2))
        if newdiff0<mindiff0:
            mindiff0=newdiff0
            closest0=node[0]
        if newdiff1<mindiff1:
            mindiff1=newdiff1
            closest1=node[0]
    return {"type":"FeatureCollection","features":[
        {"type":"Feature","geometry":{"type":"Point","coordinates":[nodes[int(closest0)][1],nodes[int(closest0)][2]]}},
        {"type":"Feature","geometry":{"type":"Point","coordinates":[nodes[int(closest1)][1],nodes[int(closest1)][2]]}}
    ]}

@app.post("/find_path/")
async def post_path(rb:RequestBody):
    mindiff0=180
    mindiff1=180
    closest0=0
    closest1=0
    for node in nodes:
        newdiff0=math.sqrt(pow(node[1]-rb.lon0,2)+pow(node[2]-rb.lat0,2))
        newdiff1=math.sqrt(pow(node[1]-rb.lon1,2)+pow(node[2]-rb.lat1,2))
        if newdiff0<mindiff0:
            mindiff0=newdiff0
            closest0=node[0]
        if newdiff1<mindiff1:
            mindiff1=newdiff1
            closest1=node[0]
    path_a1,edges_a1 = a_star(int(closest0), int(closest1), graph, False)
    response1 = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"LineString","coordinates":[]}}]}
    for node in path_a1: response1["features"][0]["geometry"]["coordinates"].append([nodes[node][1],nodes[node][2]])
    path_a2,edges_a2 = a_star(int(closest0), int(closest1), graph, True)
    response2 = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"LineString","coordinates":[]}}]}
    for node in path_a2: response2["features"][0]["geometry"]["coordinates"].append([nodes[node][1],nodes[node][2]])
    went_through = edges_a1 + edges_a2
    path_a3,edges_a3 = a_star(int(closest0), int(closest1), graph, False, went_through)
    response3 = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"LineString","coordinates":[]}}]}
    for node in path_a3: response3["features"][0]["geometry"]["coordinates"].append([nodes[node][1],nodes[node][2]])
    return [response1,response2,response3]