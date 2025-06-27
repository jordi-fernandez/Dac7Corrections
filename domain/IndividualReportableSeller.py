from dataclasses import dataclass

from domain import IndividualIdentity
from domain.RelevantActivities import RelevantActivities


@dataclass
class IndividualReportableSeller:
    identity: IndividualIdentity
    relevant_activities: list[RelevantActivities]
    doc_ref_id: str
