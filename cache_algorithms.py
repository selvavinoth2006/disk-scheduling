import pandas as pd

def fifo(pages, frame_count):
    frames = []
    faults = 0
    hits = 0
    history = []
    
    for page in pages:
        status = "Hit"
        if page not in frames:
            status = "Miss"
            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            faults += 1
        else:
            hits += 1
        history.append({'Page': page, 'Frames': list(frames), 'Status': status})
    
    return history, hits, faults

def lru(pages, frame_count):
    frames = []
    faults = 0
    hits = 0
    history = []
    
    for page in pages:
        status = "Hit"
        if page not in frames:
            status = "Miss"
            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            faults += 1
        else:
            hits += 1
            # Move hit page to the end (most recently used)
            frames.remove(page)
            frames.append(page)
        history.append({'Page': page, 'Frames': list(frames), 'Status': status})
    
    return history, hits, faults

def optimal(pages, frame_count):
    frames = []
    faults = 0
    hits = 0
    history = []
    
    for i in range(len(pages)):
        page = pages[i]
        status = "Hit"
        if page not in frames:
            status = "Miss"
            if len(frames) < frame_count:
                frames.append(page)
            else:
                # Find farthest page in future
                farthest_index = -1
                replace_index = -1
                
                for j in range(len(frames)):
                    try:
                        next_use = pages[i+1:].index(frames[j])
                    except ValueError:
                        next_use = float('inf')
                    
                    if next_use > farthest_index:
                        farthest_index = next_use
                        replace_index = j
                
                frames[replace_index] = page
            faults += 1
        else:
            hits += 1
        history.append({'Page': page, 'Frames': list(frames), 'Status': status})
        
    return history, hits, faults
