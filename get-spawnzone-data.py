import sys
import json
from spawntool import AssetData
from spawntool import GeoCoords, GeoCoordsScale
arg_mapfile = sys.argv[1]
arg_spawnfile = sys.argv[2]
arg_outputfile = sys.argv[3]

def fail_if(cond, message):
    if cond:
        print(message)
        sys.exit(1)

with open(arg_mapfile, "r") as file_handle:
    data_object = json.load(file_handle)
    MapData = AssetData(data_object)

world_settings = MapData.find_export_by_type("PrimalWorldSettings")
fail_if(world_settings is None, "File is not a map.")

print("Found world settings")
fail_if(not ("LatitudeOrigin" in world_settings \
            or "LatitudeScale" in world_settings \
            or "LongitudeOrigin" in world_settings \
            or "LongitudeScale" in world_settings), "No geocoords configuration.")
geo_coords_scale = GeoCoordsScale(
    longitude = (world_settings["LongitudeOrigin"], world_settings["LongitudeScale"]),
    latitude = (world_settings["LatitudeOrigin"], world_settings["LatitudeScale"])
)
print("Geo coords data calculated.")

with open(arg_spawnfile, "r") as file_handle:
    data_object = json.load(file_handle)
    ZoneData = AssetData(data_object)
print("Zone data loaded.")

zone_infos = {}
npc_zone_managers = ZoneData.find_exports_by_type("NPCZone")
print("Found", len(npc_zone_managers), "NPC zones")
for zone_manager in npc_zone_managers:
    body_id = int(zone_manager["BrushComponent"])
    brush = ZoneData.find_export_by_id(body_id)
    vertex_1 = brush["AggGeom"]["ConvexElems"][0]["VertexData"][0]
    vertex_x = vertex_1["x"]
    vertex_y = vertex_1["y"]
    if not "zones" in zone_manager:
        print("Invalid zone:", zone_manager["export_id"])
        continue

    for zone in zone_manager["zones"]:
        volume_bounds = zone["Spawn"]["Bounds"]
        container_name = zone["NPCSpawnEntriesContainerObject"]
        brush_actor_id = int(zone["Outer"])
        brush_actor = ZoneData.find_export_by_id(brush_actor_id)
        brush_location = brush_actor["RelativeLocation"]

        if not container_name in zone_infos.keys():
            zone_infos[container_name] = []

        location_start = geo_coords_scale.make(vertex_x + brush_location["x"], \
                                               vertex_y + brush_location["y"]).to_dict()
        location_end = geo_coords_scale.make(abs(vertex_x) + brush_location["x"], \
                                             abs(vertex_y) + brush_location["y"]).to_dict()
        spawn_location_start = geo_coords_scale.make(volume_bounds["min"]["x"], volume_bounds["min"]["y"]).to_dict()
        spawn_location_end = geo_coords_scale.make(volume_bounds["max"]["x"], volume_bounds["max"]["y"]).to_dict()
    
        zone_infos[container_name].append({
            "location": {
                "latStart": location_start["lat"],
                "longStart": location_start["long"],
                "latEnd": location_end["lat"],
                "longEnd": location_end["long"],
                "latCenter": (location_start["lat"] + location_end["lat"]) / 2,
                "longCenter": (location_start["long"] + location_end["long"]) / 2,
            },
            "spawn_location": {
                "latStart": spawn_location_start["lat"],
                "longStart": spawn_location_start["long"],
                "latEnd": spawn_location_end["lat"],
                "longEnd": spawn_location_end["long"],
                "latCenter": (spawn_location_start["lat"] + spawn_location_end["lat"]) / 2,
                "longCenter": (spawn_location_start["long"] + spawn_location_end["long"]) / 2,
            },
            "min_desired_npc_number": zone["MinDesiredNumberOfNPC"]
        })

print("Writing data to file")
final_data = {
    "geo": geo_coords_scale.to_dict(),
    "spawn_zones": zone_infos
}
with open(arg_outputfile, "w") as file_handle:
    json.dump(final_data, file_handle, indent=4)