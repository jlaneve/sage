from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ranked_command_output import RankedCommandOutput


T = TypeVar("T", bound="RetrievalAndOutput")


@_attrs_define
class RetrievalAndOutput:
    """
    Attributes:
        retrieved_docs (List['RankedCommandOutput']):
        llm_generated_code (str):
    """

    retrieved_docs: List["RankedCommandOutput"]
    llm_generated_code: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        retrieved_docs = []
        for retrieved_docs_item_data in self.retrieved_docs:
            retrieved_docs_item = retrieved_docs_item_data.to_dict()
            retrieved_docs.append(retrieved_docs_item)

        llm_generated_code = self.llm_generated_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "retrieved_docs": retrieved_docs,
                "llm_generated_code": llm_generated_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ranked_command_output import RankedCommandOutput

        d = src_dict.copy()
        retrieved_docs = []
        _retrieved_docs = d.pop("retrieved_docs")
        for retrieved_docs_item_data in _retrieved_docs:
            retrieved_docs_item = RankedCommandOutput.from_dict(retrieved_docs_item_data)

            retrieved_docs.append(retrieved_docs_item)

        llm_generated_code = d.pop("llm_generated_code")

        retrieval_and_output = cls(
            retrieved_docs=retrieved_docs,
            llm_generated_code=llm_generated_code,
        )

        retrieval_and_output.additional_properties = d
        return retrieval_and_output

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
