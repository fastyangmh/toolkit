# import
from argparse import Namespace
from os import makedirs
import xml.etree.ElementTree as ET
from os.path import join, basename
from glob import glob
from tqdm import tqdm

# def


def voc_to_yolo_format(annotations_path, labels_path):
    classes = {}

    # get xml files
    files = sorted(glob(join(annotations_path, '*.xml')))

    # parse each xml
    for f in tqdm(files):
        tree_root = ET.parse(f).getroot()
        width = int(tree_root.find('size').find('width').text)
        height = int(tree_root.find('size').find('height').text)
        with open(join(labels_path, '{}.txt'.format(basename(f)[:-4])), 'w') as text_file:
            for obj in tree_root.iter('object'):
                object_name = obj.find('name').text
                if classes.get(object_name) is None:
                    classes[object_name] = 0 if len(
                        classes) == 0 else max(classes.values())+1
                object_name = classes[object_name]
                box = {'xmin': int(obj.find('bndbox').find('xmin').text),
                       'ymin': int(obj.find('bndbox').find('ymin').text),
                       'xmax': int(obj.find('bndbox').find('xmax').text),
                       'ymax': int(obj.find('bndbox').find('ymax').text)}
                x = (box['xmin']+(box['xmax']-box['xmin'])/2)*1.0/width
                y = (box['ymin']+(box['ymax']-box['ymin'])/2)*1.0/height
                w = (box['xmax']-box['xmin'])*1.0/width
                h = (box['ymax']-box['ymin'])*1.0/height
                box = (x, y, w, h)
                text_file.write('{} {} {} {} {}\n'.format(object_name, *box))

    # write the classes to classes.txt
    with open(join(labels_path, 'classes.txt'), 'w') as text_file:
        for k, v in classes.items():
            text_file.write('{}\n'.format(k))


if __name__ == '__main__':
    # parameters
    parameters = Namespace(
        **{'data_path': './VOCdevkit/VOC2007',
           'annotations_path': 'Annotations',
           'labels_path': 'labels/',
           'classes': {}})

    # get the path and create it
    parameters.annotations_path = join(
        parameters.data_path, parameters.annotations_path)
    parameters.labels_path = join(parameters.data_path, parameters.labels_path)
    makedirs(parameters.labels_path, exist_ok=True)

    # voc to yolo format
    voc_to_yolo_format(annotations_path=parameters.annotations_path,
                       labels_path=parameters.labels_path)
