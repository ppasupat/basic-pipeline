# Plastic Case

Basic pytorch pipeline for running experiments.

Part of this is inspired by [PyText](https://github.com/facebookresearch/pytext)
and Kelvin Guu's [gtd](https://github.com/kelvinguu/lang2program/tree/master/third-party/gtd).
But instead of a pre-made Swiss Army knife,
I just want a plain plastic case that I can put my favorite blades in.

# Dependencies

* Python 3.x
* [Pytorch 1.0](https://pytorch.org/)
* [tqdm](https://pypi.org/project/tqdm/)
* (optional) [PyYAML](https://pypi.org/project/PyYAML/)
  * If not installed, only JSON configs can be used.
* (optional) [tensorboardX](https://pypi.org/project/tensorboardX/)
  * If not installed, stats will dumped to stdout instead.

# Usage

- Copy this whole thing to a new project.
- Change `yournamehere` to some awesome name (say `dogswithhorns`).
- Run
  ```bash
  sed -i 's/yournamehere/dogswithhorns/g' *.py */*.py */*/*.py
  ```
- Test with
  ```bash
  mkdir out
  ./main.py train configs/base.yml configs/data/demo.yml configs/model/demo.yml
  # Change 0.exec below to the output directory of the train command
  # Change 30 to the epoch number you want
  ./main.py test out/0.exec/config.json -l out/0.exec/30
  ```

# Implementing stuff

To implement custom data handler and model, just do what the demo ones do:

- Add a new dataset class in `data/` and add the initializer to `data/__init__.py`
- Add a new model class in `model/` and add the initializer to `model/__init__.py`

# License

None. Just copy the things you need and modify them.
