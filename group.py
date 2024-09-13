import os
import json
from copy import deepcopy
import shutil


def point_inside_box(point, box):
    x, y = point
    x1, y1 = box[0]
    x2, y2 = box[2]
    return (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1)


_dir = r'C:\Users\PC\Desktop\EDA2024\process\4'
save_dir = r'C:\Users\PC\Desktop\EDA2024\process\5'

for file in os.listdir(_dir):
    if not file.endswith('.json'):
        shutil.copy(os.path.join(_dir, file), os.path.join(save_dir, file))
        continue

    with open(os.path.join(_dir, file), "r", encoding="utf-8") as f:
        data = json.load(f)

    result = deepcopy(data)
    boxes = []
    points = []
    _group = max(list([i['group_id'] if i['group_id'] else float('-Inf') for i in data['shapes']])) + 1
    _group = 0 if _group == float('-Inf') else _group

    # First pass: identify boxes and points
    for index, shape in enumerate(result['shapes']):
        if len(shape['points']) == 4:
            if shape['group_id'] is None:
                shape['group_id'] = _group
                _group += 1
            boxes.append((index, shape['points']))
        elif len(shape['points']) == 1:
            points.append((index, shape['points'][0]))

    # Second pass: assign points to boxes
    for point_index, point in points:
        for box_index, box in boxes:
            if point_inside_box(point, box):
                result['shapes'][point_index]['group_id'] = result['shapes'][box_index]['group_id']
                break

    # Save the modified JSON file
    with open(os.path.join(save_dir, file), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
