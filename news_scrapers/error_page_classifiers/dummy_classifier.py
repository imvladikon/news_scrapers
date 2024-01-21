#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class DummyErrorPageClassifier:

    def __init__(self, **kwargs):
        pass

    def __call__(self, text):

        # for keyword in ["404", "error", "not found"]:
        #     if keyword in text:
        #         return True

        return False
