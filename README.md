# Plastic Case

Basic pytorch pipeline for running experiments.

Part of this was inspired by [PyText](https://github.com/facebookresearch/pytext)
and Kelvin Guu's [gtd](https://github.com/kelvinguu/lang2program/tree/master/third-party/gtd).
But instead of a pre-made Swiss Army knife,
I just want a plain plastic case that I can put my favorite blades into.

# Dependencies

* Python 3.x
* [Pytorch 1.0](https://pytorch.org/)
* [tqdm](https://pypi.org/project/tqdm/)
* (optional) [PyYAML](https://pypi.org/project/PyYAML/)
  * If not installed, only JSON configs can be used.
* (optional) [tensorboardX](https://pypi.org/project/tensorboardX/)
  * If not installed, stats will dumped to stdout instead.
* (optional) [bottle](https://bottlepy.org/)
  * Used for running a HTTP prediction server

# Usage

- Copy this whole thing to a new project.
- Change `yournamehere` to some awesome name (say `dogswithhorns`).
- Run
  ```bash
  sed -i 's/yournamehere/dogswithhorns/g' *.py */*.py */*/*.py
  ```
- Training:
  ```bash
  mkdir out
  ./main.py train configs/base.yml configs/data/demo.yml configs/model/demo.yml configs/debug.yml
  ```
- Test:
  ```bash
  # Change 0.exec below to the output directory of the train command
  #   and change 500 below to the step number you want
  ./main.py test out/0.exec/config.json -l out/0.exec/500
  ```
- Server:
  ```bash
  ./main.py server out/0.exec/config.json -l out/0.exec/500
  ```

# Implementing stuff

To implement your own data handler and model, just imitate the demo ones:

- Add a new dataset class in `data/` and add an initializer to `data/__init__.py`
- Add a new model class in `model/` and add an initializer to `model/__init__.py`

Right now the configs are specified by YAML or JSON with no schema whatsoever.
Feel free to replace it with a config framework of your choice.

# License

None. Just copy the things you need and modify them.
