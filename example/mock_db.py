PUBLISHED_TAGS_QUERY = [
    '000', 'cat', 'bat', 'door', 'Camera', 'floor', '001', 'car', 'train',
    'file', 'canary', 'zebra', 'dog', 'cycle', 'farm', '100', '101', '201',
    '111', '010', 'Zoo', 'Cobra', 'metal_camera', 'test_001', 'my_dog',
    'Apple', 'dog', 'egg', 'grass', 'haze', 'ink', 'joke', 'kale', 'loop',
    'most', 'nose', 'opal', 'price', 'queen', 'rake', 'steer', 'team',
    'umbrella', 'vase', 'wax', 'xylophone', 'yield'
]


def get_published_tags_from_db():
    return PUBLISHED_TAGS_QUERY


def publish_tags_to_db(tag_list):
    global PUBLISHED_TAGS_QUERY
    PUBLISHED_TAGS_QUERY = tag_list
