
###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports and set up the local path to the PyAEDT
# directory path.

import os
import modelgen

###############################################################################
# Define Location to import
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Define latitude and longitude to import.
# ansys_home = [40.273726, -80.168269]
# uncc_practice_field = [35.312504, -80.739100]
uncc_epic = [35.309925, -80.740539]
terrain_radius = 1500
# 80467.2m = 100mph*30min
###############################################################################
# Generate map and import
# ~~~~~~~~~~~~~~~~~~~~~~~
# Assign boundaries.
modeler = modelgen.ModelGenerator(None)
modeler.import_from_openstreet_map(uncc_epic,
                           terrain_radius=terrain_radius,
                           road_step=100,
                           plot_before_importing=False,
                           import_in_aedt=True)

