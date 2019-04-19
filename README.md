# Basic Pipeline

Basic pytorch pipeline for running experiments.

To use:

- Copy this whole thing to a new project.
- Change `yournamehere` to some awesome name (say `dogswithhorns`).
- Run
  ```
  sed -i 's/yournamehere/dogswithhorns/g' *.py */*.py */*/*.py
  ```
- Test with
  ```
  mkdir out
  ./main.py train configs/base.yml configs/data/demo.yml configs/model/demo.yml
  ```
