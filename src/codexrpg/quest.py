from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class QuestStatus(Enum):
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Quest:
    """Represents a sandbox quest/task."""
    id: str
    title: str
    description: str
    giver_id: str  # NPC who gives the quest
    objective: str
    reward_gold: int = 0
    reward_xp: int = 0
    status: QuestStatus = QuestStatus.AVAILABLE
    
    def accept(self):
        if self.status == QuestStatus.AVAILABLE:
            self.status = QuestStatus.ACTIVE
            return True
        return False
    
    def complete(self):
        if self.status == QuestStatus.ACTIVE:
            self.status = QuestStatus.COMPLETED
            return True
        return False


class QuestLog:
    """Tracks quests for a player."""
    def __init__(self):
        self.quests: dict[str, Quest] = {}
    
    def add_quest(self, quest: Quest):
        self.quests[quest.id] = quest
    
    def get_quest(self, quest_id: str) -> Optional[Quest]:
        return self.quests.get(quest_id)
    
    def accept_quest(self, quest_id: str) -> bool:
        quest = self.get_quest(quest_id)
        if quest:
            return quest.accept()
        return False
    
    def complete_quest(self, quest_id: str) -> bool:
        quest = self.get_quest(quest_id)
        if quest:
            return quest.complete()
        return False
    
    def get_active_quests(self) -> List[Quest]:
        return [q for q in self.quests.values() if q.status == QuestStatus.ACTIVE]
    
    def get_available_quests(self) -> List[Quest]:
        return [q for q in self.quests.values() if q.status == QuestStatus.AVAILABLE]
