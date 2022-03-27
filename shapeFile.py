import os
import json
from collections import OrderedDict

from mayaUtil.common import viewport
from mayaUtil.nurbs import curve
from pipelineUtil.fileSystem import winFile

# root where the tool tries to find all the assets and screenshots
# either hard code the full path or use env variable to set it
ROOT_PATH = ''
if not ROOT_PATH:
    ROOT_PATH = os.path.dirname(__file__)

SHAPE_PATH = os.path.join(ROOT_PATH, 'shape-library')


class ShapeFile(winFile.WinFile):

    def __init__(self, path=SHAPE_PATH):
        super(ShapeFile, self).__init__(path)

        self._metadir = os.path.join(self.directory, 'thumbnail')
        self._thumbnail = os.path.join(self._metadir, self.base+'.jpg')

    @classmethod
    def fsave(cls, transform, path):
        crv = curve.Curve.from_transform(transform)
        d = crv.to_dict()
        with open(path, "w") as f:
            try:
                json.dump(d, f, indent=4)
            except TypeError:
                # if the json file is blank, a type error will raise
                # TypeError was not handled: "must be unicode, not str"
                pass

        asset = cls(path)
        viewport.take_screenshot(asset._metadir, asset.base)
        return asset

    @classmethod
    def get_from_dir(cls, directory):
        assets = list()
        files = os.listdir(directory)
        for name in files:
            f = os.path.join(directory, name)
            if os.path.isfile(f):
                _, ext = os.path.splitext(f)
                if ext in ['.json']:
                    asset = cls(f)
                    assets.append(asset)

        return assets

    @property
    def thumbnail(self):
        return self._thumbnail

    def fimport(self):
        with open(self.path) as input_file:
            try:
                data = json.load(input_file, object_pairs_hook=OrderedDict)
                if data:
                    crv = curve.Curve.from_dict(data)
                    crv.rebuild_curve(self.base)
            except:
                pass

    def fopen(self):
        pass

    def fdelete(self):
        try:
            os.remove(self.path)
            os.remove(self.thumbnail)
        except:
            pass
