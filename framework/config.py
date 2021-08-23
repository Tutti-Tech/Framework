import os
import typing


class Config:
    def __init__(self, config_file: str = None) -> None:
        self.file_values: typing.Dict[str, str] = {}
        if config_file is not None and os.path.isfile(config_file):
            self.file_values = self._read_file(config_file)

    def __call__(
        self, key: str) -> typing.Any:
        return self.get(key)

    def get(self, key: str) -> typing.Any:
        if key in self.file_values:
            return self.file_values[key]
        raise KeyError(f"Config '{key}' is missing, and has no default.")

    def _read_file(self, file_name) -> typing.Dict[str, str]:
        file_values: typing.Dict[str, str] = {}
        with open(file_name) as input_file:
            for line in input_file.readlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    file_values[key] = value
        return file_values
