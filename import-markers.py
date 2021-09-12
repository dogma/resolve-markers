#!/usr/bin/env python

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

file = os.path.join(homeDir,"markers.json")

print("Importing markers from %s" % file)
#Do the bits
markers = Markers.readMarkers(file)
Markers.updateFolder(rootFolder, markers)
print("DONE")
