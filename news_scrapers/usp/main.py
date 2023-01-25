#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from usp.tree import sitemap_tree_for_homepage

if __name__ == '__main__':
    tree = sitemap_tree_for_homepage('https://www.israelhayom.co.il/')
    print(tree)
