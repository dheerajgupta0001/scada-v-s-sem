from typing import TypedDict
import datetime as dt


class IAppConfig(TypedDict):
    appDbConStr: str
    scadaSemFolderPath: str
