from dataclasses import dataclass

from domain import EntityIdentity
from domain.RelevantActivities import RelevantActivities


@dataclass
class EntityReportableSeller:
    identity: EntityIdentity
    relevant_activities: list[RelevantActivities]
    doc_ref_id: str
