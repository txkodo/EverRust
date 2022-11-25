from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Callable, TypeVar
from PIL import Image
from logging import getLogger

logger = getLogger(__name__)


class Blockstate:
    def __init__(
        self,
        generator: Generator,
        block: str,
        variants: dict[str, Any] | None = None,
        multipart: list[Any] | None = None,
        item: str | None = None,
    ) -> None:
        self.generator = generator
        self.block = block
        self.multipart = multipart
        self.variants = variants
        self.item = item

    def save(self):
        ns, name = self.block.split(":")
        path = self.generator.assets_path / ns / "blockstates" / (name + ".json")

        data = {}
        if self.multipart:
            data["multipart"] = self.multipart
        elif self.variants:
            data["variants"] = self.variants

        self.generator.save_json(path, data)

        itempath = self.generator.assets_path / ns / "models/item" / (name + ".json")

        if self.item is None:
            logger.warn(f"missing itemmodel for block:'{self.block}'")
        else:
            self.generator.save_json(itempath, {"parent": self.item})


class Model:
    def __init__(
        self,
        generator: Generator,
        model: str,
        parent: str | None = None,
        textures: dict[str, str] | None = None,
        elements: list[dict[str, Any]] | None = None,
    ) -> None:
        self.generator = generator
        self.model = model
        self.parent = parent
        self.textures = textures
        self.elements = elements

    def save(self):
        ns, name = self.model.split(":")
        path = self.generator.assets_path / ns / "models" / (name + ".json")
        data = {}
        if self.elements:
            data["elements"] = self.elements
        if self.parent:
            data["parent"] = self.parent
        if self.textures:
            data["textures"] = self.textures

        self.generator.save_json(path, data)


class Texture:
    def __init__(self, generator: Generator, texture: str, ctm: str | None = None) -> None:
        self.generator = generator
        self.texture = texture
        self.ctm = ctm

    def split(self, img: Image.Image, x: int, y: int):
        w = img.width
        h = img.height
        # TODO: 割り切れる保証
        ux = w // x
        uy = w // y
        return [[img.crop((ix * ux, iy * uy, (ix + 1) * ux, (iy + 1) * uy)) for ix in range(x)] for iy in range(y)]

    def splitx(self, img: Image.Image, x: int):
        w = img.width
        h = img.height
        # TODO: 割り切れ保証
        ux = w // x
        return [img.crop((ix * ux, 0, (ix + 1) * ux, h)) for ix in range(x)]

    def save_ctm(self, ctm_path: Path, imgs: list[Image.Image]):
        props = {"matchTiles": self.texture, "method": self.ctm, "tiles": f"0-{len(imgs)-1}"}
        for i, v in enumerate(imgs):
            self.generator.save_image(ctm_path / f"{i}.png", v)
            self.generator.save_props(ctm_path / f"_.properties", props)

    def save(self):
        ns, name = self.texture.split(":")
        assert name.startswith("block/")
        source_path = self.generator.blocks_path / ns / (name[6:] + ".png")
        vanilla_path = self.generator.assets_path / ns / "textures" / (name + ".png")
        ctm_path = self.generator.assets_path / ns / "optifine/ctm" / name

        match self.ctm:
            case None:
                img = Image.open(source_path)
                self.generator.save_image(vanilla_path, img)
            case "ctm_compact":
                img = Image.open(source_path)
                imgs = self.splitx(img, 5)
                self.save_ctm(ctm_path, imgs)
                self.generator.save_image(vanilla_path, imgs[0])
            case "random":
                img = Image.open(source_path)
                # TODO: 割り切れ保証
                count = img.width // img.height
                imgs = self.splitx(img, count)
                self.save_ctm(ctm_path, imgs)
                self.generator.save_image(vanilla_path, imgs[0])
            case _:
                logger.warning(f"unknown ctm type: '{self.ctm}'")


T = TypeVar("T", bound=Callable[["Generator", Any, Path], None])


class Generator:
    converter_map: dict[str, Callable[[Generator, Any, Path], None]] = {}

    def __init__(self, pack_path: Path) -> None:

        self.blocks_path = pack_path / "blocks"
        self.assets_path = pack_path / "assets"
        self.created_paths: list[Path] = []

        self.textures: dict[str, Texture] = {}
        self.models: dict[str, Model] = {}
        self.blocks: dict[str, Blockstate] = {}

    @classmethod
    def add_converter(cls, name: str):
        def inner(f: T) -> T:
            cls.converter_map[name] = f
            return f

        return inner

    def add_block(self, block: Any, dirpath: Path):

        name = block.pop("block")
        if ":" not in name:
            name = "minecraft:" + name

        for variant in block["variants"].values():
            model: str = variant["model"]
            if ":" not in model:
                ns, *parts = (dirpath / model).resolve().relative_to(self.blocks_path).parts
                variant["model"] = ns + ":block/" + "/".join(parts)

        if name in self.blocks:
            logger.warning(f'duplicate block "{name}"')
        else:
            multipart_data = block.get("multipart")
            variants_data = block.get("variants")
            item_data = block.get("item")
            if ":" not in item_data:
                    ns, *parts = (dirpath / item_data).resolve().relative_to(self.blocks_path).parts
                    item_data = ns + ":block/" + "/".join(parts)
            self.blocks[name] = Blockstate(self, name, variants_data, multipart_data, item_data)

    def add_model(self, model: Any, dirpath: Path):

        name = model.pop("model")
        if ":" not in name:
            ns, *parts = (dirpath / name).resolve().relative_to(self.blocks_path).parts
            name = ns + ":block/" + "/".join(parts)

        parent: str = model["parent"]
        if ":" not in parent:
            ns, *parts = (dirpath / parent).resolve().relative_to(self.blocks_path).parts
            model["parent"] = ns + ":block/" + "/".join(parts)

        for key in model["textures"]:
            texture: str = model["textures"][key]
            if ":" not in texture:
                ns, *parts = (dirpath / texture).resolve().relative_to(self.blocks_path).parts
                model["textures"][key] = ns + ":block/" + "/".join(parts)

        if name in self.blocks:
            logger.warning(f'duplicate model "{model["model"]}"')
        else:
            parent_data = model.get("parent")
            textures_data = model.get("textures")
            elements_data = model.get("elements")
            self.models[name] = Model(self, name, parent_data, textures_data, elements_data)

    def add_texture(self, texture: Any, dirpath: Path):
        name = texture.pop("texture")

        if ":" not in name:
            ns, *parts = (dirpath / name).resolve().relative_to(self.blocks_path).parts
            name = ns + ":block/" + "/".join(parts)

        if name in self.blocks:
            logger.warning(f'duplicate texture "{texture["texture"]}"')
        else:
            ctm_data = texture.get("ctm")
            self.textures[name] = Texture(self, name, ctm_data)

    def convert_value(self, value: Any, dirpath: Path):
        type = value.get("type")
        if type is None:
            logger.warning("object key 'type' is required.")
            return
        func = self.converter_map.get(type)
        if func is None:
            logger.warning(f"unknown convert type '{type}'.")
            return
        func(self, value, dirpath)

    def load_json(self, path: Path):
        data = json.loads(path.read_text())

        if "textures" not in data:
            data["textures"] = []

        if "models" not in data:
            data["models"] = []

        if "blocks" not in data:
            data["blocks"] = []

        if "values" not in data:
            data["values"] = []

        for value in data["values"]:
            self.convert_value(value, path.parent)

        for texture in data["textures"]:
            self.add_texture(texture, path.parent)

        for model in data["models"]:
            self.add_model(model, path.parent)

        for block in data["blocks"]:
            self.add_block(block, path.parent)

    def load_jsons(self):
        for f in self.blocks_path.glob("**/*.json"):
            self.load_json(f)

    def mkdir(self, path: Path):
        if not path.exists():
            self.mkdir(path.parent)
            path.mkdir()
            self.created_paths.append(path)

    def save_image(self, path: Path, image: Image.Image):
        self.mkdir(path.parent)
        image.save(path)
        self.created_paths.append(path)

    def save_json(self, path: Path, data: Any):
        self.mkdir(path.parent)
        path.write_text(json.dumps(data))
        self.created_paths.append(path)

    def save_props(self, path: Path, data: dict[str, str]):
        self.mkdir(path.parent)
        path.write_text("\n".join(k + "=" + v for k, v in data.items()))
        self.created_paths.append(path)

    def remove_created_files(self):
        generated_path = self.assets_path / "generated.txt"
        if not generated_path.exists():
            return
        for path in reversed(generated_path.read_text().split("\n")):
            path = self.assets_path / path
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                try:
                    path.rmdir()
                except OSError as e:
                    if e.errno != 41:
                        raise e

    def save_created_files(self):
        paths = "\n".join(str(path.relative_to(self.assets_path)) for path in self.created_paths)
        (self.assets_path / "generated.txt").write_text(paths)

    def generate(self):
        self.remove_created_files()

        self.load_jsons()

        for texture in self.textures.values():
            texture.save()

        for model in self.models.values():
            model.save()

        for block in self.blocks.values():
            block.save()

        self.save_created_files()
