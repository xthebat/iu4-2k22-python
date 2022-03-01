import sys
from os.path import basename, isdir
from pathlib import Path


class DirTree:
    """Class implementing directory tree"""
    ELBOW = "└──"
    TEE = "├──"
    PIPE_PREFIX = "│   "
    SPACE_PREFIX = "    "

    def process_dir(self, dir_name: str) -> str:
        if not self._validate_dir(dir_name):
            sys.exit("dir_tree.py:\nExpected directory name")
        dir_list = [dir_name] + self._get_directory_list(Path(dir_name))
        return dir_name + "\n" + self._prepare_for_print(dir_list[1:])

    def _validate_dir(self, dir_name: str) -> bool:
        return isdir(dir_name)

    def _get_directory_list(self, dir_path: Path) -> list:
        dir_list = []
        for file in sorted(dir_path.iterdir()):
            dir_list.append(basename(file))
            if file.is_dir():
                dir_list.append(self._get_directory_list(file))
        return dir_list

    def _prepare_for_print(self, dir_list: list, attach: str = "") -> str:
        res = ""
        for idx, file_name in enumerate(dir_list):
            if file_name:
                if isinstance(file_name, list):
                    sign = self.SPACE_PREFIX if idx == len(dir_list) - 1 else self.PIPE_PREFIX
                    res += self._prepare_for_print(file_name, attach + sign)
                else:
                    no_lists = [x for x in dir_list if not isinstance(x, list)]
                    sign = self.ELBOW if no_lists.index(file_name) == len(no_lists) - 1 else self.TEE
                    res += attach + sign + " " + file_name + "\n"
        return res


if __name__ == '__main__':
    dir_tree = DirTree()
    print(dir_tree.process_dir(sys.argv[1]))
