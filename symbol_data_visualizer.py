import json

FULL_SIZE = 400
EPS = 1e-7
BRUSH_SIZE = 0.5
SCALE = 0.1
SIZE = int(FULL_SIZE * SCALE) + 2

# Parse sketch data

with open("sample_symbol_data.json", "r") as file:
    symbol = json.loads(file.read())["rows"][0]["doc"]["data"]

grid = [[0] * SIZE for row in range(SIZE)]

# Vector operations

origin = lambda point: [point[0], point[1], 0]
dot    = lambda a, b: sum(i * j for i, j in zip(a, b))
mul    = lambda a, b: [a * i for i in b]
mag    = lambda a: pow(dot(a, a), 0.5)
add    = lambda a, b: [i + j for i, j in zip(a, b)]
sub    = lambda a, b: add(a, mul(-1, b))
vec    = lambda a, b: sub(origin(a), origin(b))

def cross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ]

proj = lambda a, b: mul(dot(a, b) / pow(mag(b), 2), b)
perp = lambda a, b: sub(a, proj(a, b))
dist = lambda a, b: mag(vec(a, b))

# Apply every stroke to the grid

def apply_stroke(a, b):
    # If the points are too close then ignore
    if dist(a, b) < EPS:
        return
    # Bounding box of stroke
    xL, xR = sorted(int(i) for i in [a[0], b[0]])
    yL, yR = sorted(int(i) for i in [a[1], b[1]])
    # Colour all cells that have a distance of < 1 cell from the line that goes from a --> b
    for y in range(yL - 1, yR + 3):
        for x in range(xL - 1, xR + 3):
            # Ignore if already painted
            if grid[y][x] == 1:
                continue
            P = [x, y, 0]
            # Vector P -> A
            PA = vec(a, P)
            # Project P onto AB
            Q = perp(PA, vec(a, b))
            # Check if point is close to AB
            if mag(Q) <= BRUSH_SIZE:
                # Check if Q lies in between A and B
                Q = add(Q, P)
                if abs((dist(Q, a) + dist(Q, b)) - dist(a, b)) < EPS:
                    grid[y][x] = 1
    return 

# Apply every stroke, then line segment sequentially
for stroke in symbol:
    points = [(point["x"] * SCALE, point["y"] * SCALE, point["t"]) for point in stroke]
    for ind in range(1, len(points)):
        apply_stroke(points[ind - 1], points[ind])

# Output the final grid
for row in grid:
    print("".join(".#"[val] for val in row))
