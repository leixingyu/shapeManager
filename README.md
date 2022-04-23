## Shape Manager

Create NURBS curves for custom controllers, then make a library out of it so you can
store and re-use them anytime.

<img src="https://i.imgur.com/iydFwTj.png" alt="ui" width=600px>

### Getting Started

1. Download and uzip the [shape-manager package](https://github.com/leixingyu/shapeManager/releases/tag/v.1.0.0) under 
`%USERPROFILE%/Documents/maya/[current maya version]/scripts/` 
or a custom directory under `PYTHONPATH` env variable.


2. Launch through script editor:

    ```python
    from shapeManager import shapeManager
    shapeManager.show()
    ```

### Dependencies

- [Qt](https://github.com/mottosso/Qt.py): a module that supports different
python qt bindings (Only needed if you need UI support functionalities)
    ```
    pip install Qt.py
    ```

Already packaged dependencies with locked version of the following,
but you could also manually clone the latest using `git clone --recursive`


- [pipelineUtil](https://github.com/leixingyu/pipelineUtil)
- [mayaUtil](https://github.com/leixingyu/mayaUtil)
- [guiUtil](https://github.com/leixingyu/guiUtil)


### How To

#### Right-Click Menu:

Load: load the selected controller in your scene
Delete: delete the selected entry in the shape library

#### Create:

Select all the nurbs curves (transform) you want to save out,
enter the name of the controller and boom!

#### Folder Structure:

All data and thumbnails live in `<ModulePath>/shape-library` folder.
In which, controller shape is stored as .json files and thumbnails
as .jpg in `thumbnail` folder.

> The pathing can be easily changed in code (`SHAPE_PATH` in _shapeFile.py_),
> but I didn't add the gui yet.

### Shape Object

A controller shape is constructed by one or more nurbs curve(s).
With each curve sharing same data structure: curve CVs, form, and degree 
represented in a .json file.

> example of _circle.json_
```json
{
    "shapes": [
        {
            "pts": [
                [
                    0.7836116248912245, 
                    4.798237340988473e-17, 
                    -0.7836116248912246
                ], 
                [
                    6.785732323110912e-17, 
                    6.785732323110912e-17, 
                    -1.1081941875543877
                ], 
                [
                    -0.7836116248912245, 
                    4.798237340988472e-17, 
                    -0.7836116248912244
                ], 
                [
                    -1.1081941875543881, 
                    3.517735619006027e-33, 
                    -5.74489823752483e-17
                ], 
                [
                    -0.7836116248912245, 
                    -4.7982373409884725e-17, 
                    0.7836116248912245
                ], 
                [
                    -1.1100856969603225e-16, 
                    -6.785732323110917e-17, 
                    1.1081941875543884
                ], 
                [
                    0.7836116248912245, 
                    -4.798237340988472e-17, 
                    0.7836116248912244
                ], 
                [
                    1.1081941875543881, 
                    -9.253679210110099e-33, 
                    1.511240500779959e-16
                ]
            ], 
            "form": 2, 
            "degree": 3
        }
    ], 
    "version": 0.1
}
```
