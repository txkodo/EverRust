from pathlib import Path
from __python__.base import Generator
import __python__.cube

Generator(Path(__file__).parent.parent).generate()
