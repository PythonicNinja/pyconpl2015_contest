import re


re_rect = re.compile('\<rect\s+fill="(?P<type>\w+)"\s+height="(?P<height>\d+)"\s+width="(?P<width>\d+)"\s+x="(?P<x>\d+)"\s+y="(?P<y>\d+)"><\/rect>')

maze_html = open('maze.html', 'r')

walls = []

for type, height, width, x, y in re_rect.findall(maze_html.read()):
    x = int(x)
    y = int(y)
    height = int(height)
    if type == 'black':
        walls.append((x/height, y/height))


print walls




