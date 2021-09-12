#!/usr/bin/env python

import json
import hashlib
import os
import Markers

# import DaVinciResolveScript as dvr_script
# resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()

homeDir = str(os.path.expanduser("~"))
print("Home Dir: %s" % homeDir)


# Could daisy chain these but I want the individual objects for laterz
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
mp = project.GetMediaPool()
rootFolder = mp.GetRootFolder()

#Intialize a dictionary to use for storing all the 
clipMarkers = {}

#Do the bits
Markers.exportFolder(rootFolder, clipMarkers)
Markers.writeMarkers(os.path.join(homeDir,"markers.json"),clipMarkers)
print("Exported to %s" % os.path.join(homeDir,"markers.json"))
print("DONE")
