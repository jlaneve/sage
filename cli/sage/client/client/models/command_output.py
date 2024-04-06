from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CommandOutput")


@_attrs_define
class CommandOutput:
    """
    Attributes:
        command (str):
        cwd (str):
        base_dir (str):
        user (str):
        timestamp (str):
        command_summary (str):
    """

    command: str
    cwd: str
    base_dir: str
    user: str
    timestamp: str
    command_summary: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command = self.command

        cwd = self.cwd

        base_dir = self.base_dir

        user = self.user

        timestamp = self.timestamp

        command_summary = self.command_summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command": command,
                "cwd": cwd,
                "base_dir": base_dir,
                "user": user,
                "timestamp": timestamp,
                "command_summary": command_summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        command = d.pop("command")

        cwd = d.pop("cwd")

        base_dir = d.pop("base_dir")

        user = d.pop("user")

        timestamp = d.pop("timestamp")

        command_summary = d.pop("command_summary")

        command_output = cls(
            command=command,
            cwd=cwd,
            base_dir=base_dir,
            user=user,
            timestamp=timestamp,
            command_summary=command_summary,
        )

        command_output.additional_properties = d
        return command_output

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
