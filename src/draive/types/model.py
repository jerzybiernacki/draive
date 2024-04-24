import json
from dataclasses import asdict
from datetime import datetime
from typing import Any, Self
from uuid import UUID

from draive.helpers import Missing
from draive.parameters import ParametrizedData

__all__ = [
    "Model",
]


class ModelJSONEncoder(json.JSONEncoder):
    def default(self, o: object) -> Any:
        if isinstance(o, Missing):
            return None
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, UUID):
            return o.hex
        else:
            return json.JSONEncoder.default(self, o)


class Model(ParametrizedData):
    @classmethod
    def specification(cls) -> str:
        return cls.__parameters_definition__.specification

    @classmethod
    def from_json(
        cls,
        value: str | bytes,
        decoder: type[json.JSONDecoder] = json.JSONDecoder,
    ) -> Self:
        try:
            return cls.validated(
                **json.loads(
                    value,
                    cls=decoder,
                )
            )

        except Exception as exc:
            raise ValueError(f"Failed to decode {cls.__name__} from json:\n{value}") from exc

    def as_json(
        self,
        aliased: bool = True,
        indent: int | None = None,
        encoder_class: type[json.JSONEncoder] = ModelJSONEncoder,
    ) -> str:
        try:
            return json.dumps(
                self.as_dict(aliased=aliased),
                indent=indent,
                cls=encoder_class,
            )

        except Exception as exc:
            raise ValueError(
                f"Failed to encode {self.__class__.__name__} to json:\n{asdict(self)}"
            ) from exc

    def __str__(self) -> str:
        return self.as_json(
            aliased=True,
            indent=2,
        )
