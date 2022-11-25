from pathlib import Path
from typing import Any
from __python__.base import Generator, logger


@Generator.add_converter("cube")
def cube(gen: Generator, data: Any, dirpath: Path):
    block = data.get("block")
    if block is None:
        logger.warning(f"missing key 'block'. ({data})")
        return
    model = data.get("model")
    if model is None:
        logger.warning(f"missing key 'model'. ({data})")
        return
    textures: dict[str, str] = data.get("textures")
    if textures is None:
        logger.warning(f"missing key 'textures'. ({data})")
        return

    gen.add_block({"block": block, "variants": {"": {"model": model}}, "item": model}, dirpath)

    keys = textures.keys()
    if keys == {"end", "side"}:
        gen.add_model(
            {
                "model": model,
                "parent": "minecraft:block/cube_column",
                "textures": {"end": textures["end"], "side": textures["side"]},
            },
            dirpath,
        )
    elif keys == {"all"}:
        gen.add_model(
            {"model": model, "parent": "minecraft:block/cube_all", "textures": {"all": textures["all"]}}, dirpath
        )
    elif keys == {"top", "bottom", "side"}:
        gen.add_model(
            {
                "model": model,
                "parent": "minecraft:block/cube_bottom_top",
                "textures": {"top": textures["top"], "bottom": textures["bottom"], "side": textures["side"]},
            },
            dirpath,
        )
    else:
        logger.warning(f"unknown texture key pattern for cube: {textures}")
        return


@Generator.add_converter("slab")
def slab(gen: Generator, data: Any, dirpath: Path):
    block = data.get("block")
    if block is None:
        logger.warning(f"missing key 'block'. ({data})")
        return
    model = data.get("model")
    if model is None:
        logger.warning(f"missing key 'model'. ({data})")
        return

    top: dict[str, str] = data.get("top")
    bottom: dict[str, str] = data.get("bottom")
    double: dict[str, str] = data.get("double")

    textures: dict[str, str] = data.get("textures")
    if textures is None:
        if top is None or bottom is None or double is None:
            logger.warning(f"missing key 'textures'. ({data})")
            return
    else:
        keys = textures.keys()
        if keys == {"end", "side"}:
            textures = {"top": textures["end"], "bottom": textures["end"], "side": textures["side"]}
        elif keys == {"all"}:
            textures = {"top": textures["all"], "bottom": textures["all"], "side": textures["all"]}
        elif keys == {"top", "bottom", "side"}:
            pass
        else:
            logger.warning(f"unknown texture key pattern for slab: {textures}")
            return

    if top is None:
        top = model + "_top"
        gen.add_model({"model": top, "parent": "minecraft:block/slab_top", "textures": textures}, dirpath)
    if bottom is None:
        bottom = model + "_bottom"
        gen.add_model({"model": bottom, "parent": "minecraft:block/slab", "textures": textures}, dirpath)
    if double is None:
        double = model + "_double"
        gen.add_model({"model": double, "parent": "minecraft:block/cube_bottom_top", "textures": textures}, dirpath)

    block_data = {
        "block": block,
        "item": bottom,
        "variants": {
            "type=bottom": {"model": bottom},
            "type=double": {"model": double},
            "type=top": {"model": top},
        },
    }
    gen.add_block(block_data, dirpath)


@Generator.add_converter("stairs")
def stairs(gen: Generator, data: Any, dirpath: Path):
    block = data.get("block")
    if block is None:
        logger.warning(f"missing key 'block'. ({data})")
        return
    model = data.get("model")
    if model is None:
        logger.warning(f"missing key 'model'. ({data})")
        return

    straight: dict[str, str] = data.get("straight")
    inner: dict[str, str] = data.get("inner")
    outer: dict[str, str] = data.get("outer")

    textures: dict[str, str] = data.get("textures")
    if textures is None:
        if straight is None or inner is None or outer is None:
            logger.warning(f"missing key 'textures'. ({data})")
            return
    else:
        keys = textures.keys()
        if keys == {"end", "side"}:
            textures = {"top": textures["end"], "bottom": textures["end"], "side": textures["side"]}
        elif keys == {"all"}:
            textures = {"top": textures["all"], "bottom": textures["all"], "side": textures["all"]}
        elif keys == {"top", "bottom", "side"}:
            pass
        else:
            logger.warning(f"unknown texture key pattern for stair: {textures}")
            return

    if straight is None:
        straight = model
        gen.add_model({"model": straight, "parent": "minecraft:block/stairs", "textures": textures}, dirpath)
    if inner is None:
        inner = model + "_inner"
        gen.add_model({"model": inner, "parent": "minecraft:block/inner_stairs", "textures": textures}, dirpath)
    if outer is None:
        outer = model + "_outer"
        gen.add_model({"model": outer, "parent": "minecraft:block/outer_stairs", "textures": textures}, dirpath)

    block_data = {
        "block": block,
        "item": straight,
        "variants": {
            "facing=east,half=bottom,shape=inner_left": {
                "model": inner,
                "y": 270,
                "uvlock": True,
            },
            "facing=east,half=bottom,shape=inner_right": {"model": inner},
            "facing=east,half=bottom,shape=outer_left": {
                "model": outer,
                "y": 270,
                "uvlock": True,
            },
            "facing=east,half=bottom,shape=outer_right": {"model": outer},
            "facing=east,half=bottom,shape=straight": {"model": straight},
            "facing=east,half=top,shape=inner_left": {
                "model": inner,
                "x": 180,
                "uvlock": True,
            },
            "facing=east,half=top,shape=inner_right": {
                "model": inner,
                "x": 180,
                "y": 90,
                "uvlock": True,
            },
            "facing=east,half=top,shape=outer_left": {
                "model": outer,
                "x": 180,
                "uvlock": True,
            },
            "facing=east,half=top,shape=outer_right": {
                "model": outer,
                "x": 180,
                "y": 90,
                "uvlock": True,
            },
            "facing=east,half=top,shape=straight": {
                "model": straight,
                "x": 180,
                "uvlock": True,
            },
            "facing=north,half=bottom,shape=inner_left": {
                "model": inner,
                "y": 180,
                "uvlock": True,
            },
            "facing=north,half=bottom,shape=inner_right": {
                "model": inner,
                "y": 270,
                "uvlock": True,
            },
            "facing=north,half=bottom,shape=outer_left": {
                "model": outer,
                "y": 180,
                "uvlock": True,
            },
            "facing=north,half=bottom,shape=outer_right": {
                "model": outer,
                "y": 270,
                "uvlock": True,
            },
            "facing=north,half=bottom,shape=straight": {
                "model": straight,
                "y": 270,
                "uvlock": True,
            },
            "facing=north,half=top,shape=inner_left": {
                "model": inner,
                "x": 180,
                "y": 270,
                "uvlock": True,
            },
            "facing=north,half=top,shape=inner_right": {
                "model": inner,
                "x": 180,
                "uvlock": True,
            },
            "facing=north,half=top,shape=outer_left": {
                "model": outer,
                "x": 180,
                "y": 270,
                "uvlock": True,
            },
            "facing=north,half=top,shape=outer_right": {
                "model": outer,
                "x": 180,
                "uvlock": True,
            },
            "facing=north,half=top,shape=straight": {
                "model": straight,
                "x": 180,
                "y": 270,
                "uvlock": True,
            },
            "facing=south,half=bottom,shape=inner_left": {"model": inner},
            "facing=south,half=bottom,shape=inner_right": {
                "model": inner,
                "y": 90,
                "uvlock": True,
            },
            "facing=south,half=bottom,shape=outer_left": {"model": outer},
            "facing=south,half=bottom,shape=outer_right": {
                "model": outer,
                "y": 90,
                "uvlock": True,
            },
            "facing=south,half=bottom,shape=straight": {
                "model": straight,
                "y": 90,
                "uvlock": True,
            },
            "facing=south,half=top,shape=inner_left": {
                "model": inner,
                "x": 180,
                "y": 90,
                "uvlock": True,
            },
            "facing=south,half=top,shape=inner_right": {
                "model": inner,
                "x": 180,
                "y": 180,
                "uvlock": True,
            },
            "facing=south,half=top,shape=outer_left": {
                "model": outer,
                "x": 180,
                "y": 90,
                "uvlock": True,
            },
            "facing=south,half=top,shape=outer_right": {
                "model": outer,
                "x": 180,
                "y": 180,
                "uvlock": True,
            },
            "facing=south,half=top,shape=straight": {
                "model": straight,
                "x": 180,
                "y": 90,
                "uvlock": True,
            },
            "facing=west,half=bottom,shape=inner_left": {
                "model": inner,
                "y": 90,
                "uvlock": True,
            },
            "facing=west,half=bottom,shape=inner_right": {
                "model": inner,
                "y": 180,
                "uvlock": True,
            },
            "facing=west,half=bottom,shape=outer_left": {
                "model": outer,
                "y": 90,
                "uvlock": True,
            },
            "facing=west,half=bottom,shape=outer_right": {
                "model": outer,
                "y": 180,
                "uvlock": True,
            },
            "facing=west,half=bottom,shape=straight": {
                "model": straight,
                "y": 180,
                "uvlock": True,
            },
            "facing=west,half=top,shape=inner_left": {
                "model": inner,
                "x": 180,
                "y": 180,
                "uvlock": True,
            },
            "facing=west,half=top,shape=inner_right": {
                "model": inner,
                "x": 180,
                "y": 270,
                "uvlock": True,
            },
            "facing=west,half=top,shape=outer_left": {
                "model": outer,
                "x": 180,
                "y": 180,
                "uvlock": True,
            },
            "facing=west,half=top,shape=outer_right": {
                "model": outer,
                "x": 180,
                "y": 270,
                "uvlock": True,
            },
            "facing=west,half=top,shape=straight": {
                "model": straight,
                "x": 180,
                "y": 180,
                "uvlock": True,
            },
        },
    }
    gen.add_block(block_data, dirpath)


@Generator.add_converter("generic")
def generic(gen: Generator, data: Any, dirpath: Path):
    cube(gen, data | {"model": data["model"] + "_block"}, dirpath)
    slab(gen, data | {"block": data["slab"], "model": data["model"] + "_slab"}, dirpath)
    stairs(gen, data | {"block": data["stairs"], "model": data["model"] + "_stair"}, dirpath)
