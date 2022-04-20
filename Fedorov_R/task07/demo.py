import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Dict, List, Optional, Tuple

import pandas as pd
from awpy import DemoParser

from functions import slice2range


pd.options.mode.chained_assignment = None  # default='warn'


def clear_rounds(df: pd.DataFrame) -> Tuple[int, pd.DataFrame]:
    df = df.loc[df.winningTeam.notna()]
    df.reset_index(inplace=True, drop=True)

    start_idx = ((df.tScore == 0) & (df.ctScore == 0)).idxmin() - 1

    offset = df.roundNum[start_idx] - 1

    df = df[start_idx:]

    df.roundNum = df.roundNum - offset

    df.reset_index(inplace=True, drop=True)
    df.sort_values(by="roundNum", ascending=True, inplace=True)

    return offset, df


def clear_data(df: pd.DataFrame, offset: int, rounds: pd.DataFrame) -> pd.DataFrame:
    if "attackerName" in df:
        df = df.loc[df.attackerName.notna()]

    df.roundNum = df.roundNum - offset

    df = df[df.roundNum.isin(rounds.roundNum)]
    df.reset_index(inplace=True, drop=True)

    return df


@dataclass
class Demo:
    dem_path: Path
    json_path: Path

    rounds: pd.DataFrame
    damages: pd.DataFrame
    kills: pd.DataFrame
    flashes: pd.DataFrame
    weapons_fires: pd.DataFrame
    grenades: pd.DataFrame

    frames: pd.DataFrame

    @classmethod
    def load(cls, demo_path: Union[Path, str], force: bool = False, parse_rate: Optional[int] = None):
        demo_path = Path(demo_path)

        out_path = demo_path.parent

        json_path = Path(out_path, demo_path.stem).with_suffix(".json")

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

        if force or not json_path.is_file():
            # output results to a dictionary of dataframes.
            demo: Dict[str, pd.DataFrame] = demo_parser.parse(return_type="df")
        else:
            # read to also internal state... why
            demo_parser.read_json(str(json_path))
            demo: Dict[str, pd.DataFrame] = demo_parser.parse_json_to_df()

        return Demo(
            demo_path,
            json_path,
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
            rounds = (self.__rounds[it] for it in slice2range(item))
            return pd.concat(rounds, ignore_index=True)
        elif isinstance(item, int):
            return self.__rounds[item]
        else:
            raise TypeError("item must slice or int")

    def __iter__(self):
        return self.__rounds.__iter__()

    def items(self):
        return self.__rounds.items()