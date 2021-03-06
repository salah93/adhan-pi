from typing import Dict, Optional

import requests


class AdhanPiError(Exception):
    pass


class PrayerAPIError(AdhanPiError):
    def __init__(
        self,
        response: Optional[requests.Response] = None,
        data: Optional[Dict] = None,
    ):
        if response:
            super().__init__(
                "Could not find prayertimes status={status}".format(
                    status=response.status_code
                )
            )
        elif data:
            super().__init__(
                "Could not find prayertimes data={data}".format(data=data)
            )
        else:
            super().__init__()


class LocationNotFoundError(AdhanPiError):
    def __init__(self, query: str):
        super().__init__("Could not find location for {}".format(query))
