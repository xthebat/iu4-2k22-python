import gzip
import os
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Optional, Type, Union, List

import pandas as pd
from awpy import DemoParser


def _slice2range(s: slice, length=2 ** 32) -> range:
    return range(*s.indices(length))


@dataclass
class Demo:
    rounds: pd.DataFrame
    damages: pd.DataFrame
    kills: pd.DataFrame
    flashes: pd.DataFrame
    weapons_fires: pd.DataFrame
    grenades: pd.DataFrame

    frames: pd.DataFrame

    @classmethod
    def from_dict(cls, demo):
        return Demo(
            rounds=demo["rounds"],
            damages=demo["damages"],
            kills=demo["kills"],
            flashes=demo["flashes"],
            weapons_fires=demo["weaponFires"],
            grenades=demo["grenades"],
            frames=demo.get("playerFrames", None)
        )


@dataclass
class Frames:
    __rounds: Dict[int, pd.DataFrame]

    @classmethod
    def from_demo(cls, demo: Demo):
        rounds = {num: group.reset_index(drop=True) for num, group in demo.frames.groupby(by="roundNum")}
        return Frames(rounds)

    @classmethod
    def from_zip(cls, path: Union[Path, str], to_load: Optional[List[int]] = None):
        rounds = dict()
        path = Path(path)
        with zipfile.ZipFile(str(path), "r") as file:
            for name in file.namelist():
                stem = Path(name).stem
                num = int(stem)
                if to_load is None or num in to_load:
                    text = file.read(name).decode("utf-8")
                    rounds[num] = pd.read_json(text).reset_index(drop=True)
        return Frames(rounds)

    def dump(self, path: Union[Path, str], to_save: Optional[List[int]] = None):
        path = Path(path)
        with zipfile.ZipFile(str(path), "w") as file:
            for num, df in self.__rounds.items():
                name = f"{num}.json"
                if to_save is None or num in to_save:
                    data = df.to_json()
                    file.writestr(name, data, compresslevel=9)
        return self

    def __getitem__(self, item: Union[slice, int]):
        if isinstance(item, slice):
            rounds = (self.__rounds[it] for it in _slice2range(item))
            return pd.concat(rounds, ignore_index=True)
        elif isinstance(item, int):
            return self.__rounds[item]
        else:
            raise TypeError("item must slice or int")

    def __iter__(self):
        return self.__rounds.__iter__()

    def items(self):
        return self.__rounds.items()


class AbstractDemoParser:

    def __init__(self, registry: "ParserRegistry"):
        self._registry = registry

    def parse(self, file_path: str, parse_rate=None) -> Demo:
        raise NotImplementedError


@dataclass
class DemDemoParser(AbstractDemoParser):
    _registry: "ParserRegistry"

    def parse(self, file_path: str, parse_rate=None) -> Demo:
        demo_path = Path(file_path)

        out_path = demo_path.parent

        demo_parser = DemoParser(
            demofile=str(demo_path.absolute()).replace("\\", "/"),
            log=True,
            # TODO: there is bug in DemoParser.parse_demo() in self.output_file ... lead to ERROR logging
            outpath=str(out_path.absolute()).replace("\\", "/"),
            trade_time=5,
            buy_style="hltv",
            json_indentation=False,
            parse_frames=parse_rate is not None,
            parse_rate=parse_rate or 128
        )

        demo: Dict[str, pd.DataFrame] = demo_parser.parse(return_type="df")

        return Demo.from_dict(demo)


@dataclass
class JsonDemoParser(AbstractDemoParser):
    _registry: "ParserRegistry"

    def parse(self, file_path: str, parse_rate=None) -> Demo:
        demo_parser = DemoParser()
        demo_parser.read_json(file_path)
        demo: Dict[str, pd.DataFrame] = demo_parser.parse_json_to_df()
        return Demo.from_dict(demo)


class GzDemoParser(AbstractDemoParser):
    _registry: "ParserRegistry"

    def parse(self, file_path: str, parse_rate=None) -> Demo:
        path = Path(file_path)
        file = NamedTemporaryFile(delete=False, suffix=Path(path.stem).suffix)
        with gzip.open(file_path, 'rb') as f_in:
            with open(file.name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        file.close()
        demo = self._registry.parse(file.name, parse_rate)
        os.unlink(file.name)
        return demo


DemoParserInterfaceType = Type[AbstractDemoParser]


class ParserRegistry:

    @dataclass
    class ParserNotFoundException(Exception):
        suffix: str

    def __init__(self):
        self.__parser: Dict[str, DemoParserInterfaceType] = dict()

    def register(self, suffix: str, parser: DemoParserInterfaceType):
        assert suffix not in self.__parser, f"Parser for format {suffix} already registered!"
        self.__parser[suffix] = parser
        return self

    def __getitem__(self, item: str):
        if item not in self.__parser:
            raise ParserRegistry.ParserNotFoundException(item)
        return self.__parser[item]

    def parse(self, file_path: str, parse_rate=None) -> Demo:
        suffix = Path(file_path).suffix
        parser_type = self[suffix]
        parser = parser_type(self)
        return parser.parse(file_path, parse_rate)

    def parse_or_none(self, file_path: str) -> Optional[Demo]:
        try:
            return self.parse(file_path)
        except ParserRegistry.ParserNotFoundException:
            return None


