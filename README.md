# pyqt_tag_manager

---
## Description
A dynamic Tag management widget with custom sorting and focus features.

Tag Manager allows both editable and read-only modes:
<p align="center">
  <img src="/docs/images/1.PNG">
</p>

While in editing mode, items are sorted dynamically to prioritize the results matching the input 
text:
<p align="center">
  <img src="/docs/images/2.PNG">
</p>

---
## Example
Run `../example/launch_ui_example.bat` for a simple test GUI to play around with.

If neither `Qt.Py` or `PySide2` are available, replace the `PySide2` imports in `__init__.py` to `PyQt5`.

---
## Usage
```python
from pyqt_tag_manager.tag_manager import TagManager
...

tag_manager = TagManager()
tag_manager.add_tags(['ace', '000', 'zoo', 'cat', '10'])
```
