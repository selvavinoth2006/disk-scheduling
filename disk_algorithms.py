def fcfs(requests, head):
    sequence = [head] + requests
    distance = 0
    for i in range(1, len(sequence)):
        distance += abs(sequence[i] - sequence[i-1])
    return sequence, distance

def sstf(requests, head):
    sequence = [head]
    requests = list(requests)
    distance = 0
    current_head = head
    
    while requests:
        closest = min(requests, key=lambda x: abs(x - current_head))
        distance += abs(closest - current_head)
        current_head = closest
        sequence.append(current_head)
        requests.remove(closest)
        
    return sequence, distance

def scan(requests, head, direction="left", max_track=199):
    sequence = [head]
    distance = 0
    requests = sorted(requests)
    
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    if direction == "left":
        # Visit left elements, then the end (0), then right elements
        path = left[::-1] + [0] + right
    else:
        # Visit right elements, then the end (max), then left elements
        path = right + [max_track] + left[::-1]
        
    for p in path:
        distance += abs(p - sequence[-1])
        sequence.append(p)
        
    return sequence, distance

def cscan(requests, head, direction="right", max_track=199):
    sequence = [head]
    distance = 0
    requests = sorted(requests)
    
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    if direction == "right":
        # Visit right, jump to 0, visit left
        path = right + [max_track, 0] + left
    else:
        # Visit left, jump to max, visit right
        path = left[::-1] + [0, max_track] + right[::-1]
        
    for p in path:
        distance += abs(p - sequence[-1])
        sequence.append(p)
        
    return sequence, distance
