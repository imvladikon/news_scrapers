#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


class RandomUserAgentService:
    def __init__(self, software_names=None, operating_systems=None):
        if operating_systems is None:
            operating_systems = [
                OperatingSystem.WINDOWS.value,
                OperatingSystem.LINUX.value,
            ]
        if software_names is None:
            software_names = [SoftwareName.CHROME.value, SoftwareName.GOOGLEBOT.value]
        self.user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=100
        )

    def get(self):
        return self.user_agent_rotator.get_random_user_agent()


if __name__ == '__main__':
    user_agent_service = RandomUserAgentService()
    for _ in range(10):
        print(user_agent_service.get())
