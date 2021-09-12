import hashlib
import re
import json

def updateFolder(folder, clipMarkers):
    """Recursive function used to walk through the folder and update all markers found that match the clipMarkers provided"""
    print("Importing markers for all Media Items in %s" % folder.GetName())

    for clip in folder.GetClipList():
        clipId = clip.GetMediaId()
        if clipId in clipMarkers:
            #We have markers for this clip.
            updateClip(clip, clipMarkers[clipId])

    for child in folder.GetSubFolderList():
        updateFolder(child, clipMarkers)

def updateClip(clip, markers):
    """Update a clips markers, using the provided markers"""
    print("Updating clip %s" % clip.GetName())
    # existingMarkers = clip.GetMarkers()
    #Delete all existing markers
    # for key in existingMarkers:
    #     print("Removing marker from frame %s" % key)
    #     clip.DeleteMarkerAtFrame(key)

    for key in markers:
        print("Adding new marker %s to frame %s" % (markers[key]['name'], key))
        clip.DeleteMarkerAtFrame(int(key))
        if clip.AddMarker(int(key), markers[key]['color'],markers[key]['name'],markers[key]['note'],markers[key]['duration']):
            print("Succeeded adding %s " % key)
        else:
            print("Failed to add marker to %s" % key)

def exportFolder(folder, clipMarkers):
    """Recursive function used to walk through all items in this folder, and extract the markers from it."""

    print("Processing folder %s" % (folder.GetName()))
    children = folder.GetSubFolderList()
    clips = folder.GetClipList()

    #Do the clips
    for clip in clips:
        print("Processing clip %s" % clip.GetName())
        clipId = clip.GetMediaId()
        markers = exportClip(clip)
        clipMarkers[clipId] = markers

    for child in children:
        exportFolder(child, clipMarkers)

def exportClip(clip):
    """Extract the markers from the given clip and add any missing sync markers at the same time."""
    markers = clip.GetMarkers()
    for key in markers:
        if checkMarkerForTags(markers[key]) == None:
            print("Adding SYNC key")
            addMarkerKey(markers[key])
    return markers

def checkMarkerForTags(marker):
    """Checks the marker for an existing sync tag. The sync tag is used to idenify the marker should it move to a different timecode."""
    noteLen = len(marker['note'])
    print("Note: %s" % marker['note'])
    if noteLen >= 12:            
        keyMarker = marker['note'][(noteLen - 12):][:4]
        print("Key Marker is %s" % keyMarker)
        key = marker['note'][(noteLen - 8):]
        print("Sync Key is %s" % key)
        if(keyMarker == "SYN:"):
            return key
    return None

def addMarkerKey(marker):
    """Generates an 8 character key for the provided marker and appends it to the note part of the marker"""
    md5 = hashlib.md5()
    markerString = json.dumps(marker)
    md5.update(markerString.encode('utf-8'))
    hash = md5.hexdigest()[:8]
    marker['note'] += "\n\nSYN:%s" % hash

def readMarkers(file):
    print("Opening file %s" % file)
    markers = ""
    with open(file,"r") as target:
        for line in target:
            markers += line

    return json.loads(markers)

def writeMarkers(file, markerDb):
    with open(file,"w") as f:
        f.writelines(json.dumps(markerDb))