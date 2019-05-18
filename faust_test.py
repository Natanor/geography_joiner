import asyncio

import faust
from shapely import wkt

from main import find_intersections
from random_polygon import random_polygon
from utils import read_pickle


class Geography(faust.Record):
    wkt: str


class GFID(faust.Record):
    gfid: str





app = faust.App("location-joiner-app", broker='kafka://localhost',
             )
input_topic = app.topic("geographys_to_join", value_type=Geography)
output_topic = app.topic("gfids", value_type=GFID)

buildings = read_pickle("rnd_dict.pkl")

@app.agent(input_topic)
async def join(geographys):
    async for geography in geographys:
        gfids = find_intersections(buildings, wkt.loads(geography.wkt))
        if len(gfids) > 0:
            await asyncio.wait([output_topic.send(value=GFID(gfid[0]["id"])) for gfid in gfids])





# @app.agent(output_topic)
# async def output(GFIDS):
#     async for gfid in GFIDS:
#         print(gfid.gfid)

@app.timer(interval=5.0)
async def example_sender():
    await asyncio.wait([input_topic.send(value=Geography( random_polygon().wkt)) for i in range(100)])

if __name__ == '__main__':
    app.main()