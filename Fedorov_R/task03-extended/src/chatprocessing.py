from collections import defaultdict
from typing import Dict, List

from userwidget import UserUnit, NicknameType, MessageType


ChatProcessingDict = Dict[NicknameType, MessageType]
ChatProcessingList = List[UserUnit]


class ChatProcessing:

    def __init__(self):
        self.processed_recording = defaultdict(MessageType)

    def process_list(self, recording: str) -> ChatProcessingList:
        recording_dict = self.process(recording)
        recording_list = list()
        for nickname, messages in recording_dict.items():
            recording_list.append(UserUnit(nickname, messages))
        return recording_list

    def process_dict(self, recording: str) -> ChatProcessingDict:
        return self.process(recording)

    def process(self, recording: str) -> ChatProcessingDict:
        self.processed_recording.clear()
        recording_list = recording.replace('\u200b', '').split('\n')
        cleared_recording_list = [s for s in recording_list if s != '']
        for i in range(0, len(cleared_recording_list), 2):
            self.processed_recording[cleared_recording_list[i]].append(cleared_recording_list[i + 1])
        return dict(self.processed_recording)

