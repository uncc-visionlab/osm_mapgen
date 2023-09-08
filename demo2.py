###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports and set up the local path to the PyAEDT
# directory path.

import json
import os
import logging
import sys

from osm import BuildingsPrep
from osm import RoadPrep
from osm import TerrainPrep

###############################################################################
# Define Location to import
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Define latitude and longitude to import.
# ansys_home = [40.273726, -80.168269]
# uncc_practice_field = [35.312504, -80.739100]
latitude_longitude = [35.309925, -80.740539]
terrain_radius = 100
output_path = "."
include_srtm_terrain = False
include_osm_buildings = True
include_osm_roads = False
min_elevation_shift = 0
env_name="demo2"
###############################################################################
# Generate map and import
# ~~~~~~~~~~~~~~~~~~~~~~~
# Assign boundaries.

# output_path = self._app.working_directory
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
parts_dict = {}
terrain_mesh = None
# instantiate terrain module
if include_srtm_terrain:
    logger.info("Generating Terrain Geometry")
    terrain_prep = TerrainPrep(cad_path=output_path)
    terrain_geo = terrain_prep.get_terrain(latitude_longitude, max_radius=terrain_radius, grid_size=30)
    terrain_stl = terrain_geo["file_name"]
    terrain_mesh = terrain_geo["mesh"]
    terrain_dict = {"file_name": terrain_stl, "color": "brown", "material": "earth"}
    parts_dict["terrain"] = terrain_dict
    building_mesh = None
    road_mesh = None

# import vtk
# polygon = vtk.Polygon()

if include_osm_buildings:
    logger.info("Generating Building Geometry")
    building_prep = BuildingsPrep(cad_path=output_path)
    building_geo = building_prep.generate_buildings(
        latitude_longitude, terrain_mesh, max_radius=terrain_radius * 0.8
    )
    building_stl = building_geo["file_name"]
    building_mesh = building_geo["mesh"]
    building_dict = {"file_name": building_stl, "color": "grey", "material": "concrete"}
    parts_dict["buildings"] = building_dict

if include_osm_roads:
    logger.info("Generating Road Geometry")
    road_prep = RoadPrep(cad_path=output_path)
    road_geo = road_prep.create_roads(
        latitude_longitude,
        terrain_mesh,
        max_radius=terrain_radius,
        z_offset=z_offset,
        road_step=road_step,
        road_width=road_width,
    )

    road_stl = road_geo["file_name"]
    road_mesh = road_geo["mesh"]
    road_dict = {"file_name": road_stl, "color": "black", "material": "asphalt"}
    parts_dict["roads"] = road_dict

json_path = os.path.join(output_path, env_name + ".json")
terrain_bounds = None
if (terrain_mesh):
    terrain_bounds = terrain_mesh.bounds
building_bounds = None
if (building_mesh):
    building_bounds = building_mesh.bounds
scene = {
    "name": env_name,
    "version": 1,
    "type": "environment",
    "center_lat_lon": latitude_longitude,
    "radius": terrain_radius,
    "include_terrain": include_srtm_terrain,
    "terrain_bounds": terrain_bounds,
    "include_buildings": include_osm_buildings,
    "buildings_bounds": building_bounds,
    "include_roads": include_osm_roads,
    "parts": parts_dict,
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(scene, f, indent=4)

logger.info("Done...")
