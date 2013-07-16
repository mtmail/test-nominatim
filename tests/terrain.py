from lettuce import world
import os

world.base_url = os.environ['NOMINATIM_SERVER']
