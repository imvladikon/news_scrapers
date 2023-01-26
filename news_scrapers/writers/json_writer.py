#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class JsonWriter:


    def __init__(self, output_file):
        self.output_file = output_file
        self.f_handler = None


    def __enter__(self):
        self.f_handler = open(self.output_file, "w")
        return self

    def write(self, obj):
        self.f_handler.write(obj)
        self.f_handler.write("\n")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f_handler.close()
