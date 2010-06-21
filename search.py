#!/usr/bin/env python
"""
Created by: Michael Yanovich

Copyright 2010, Michael Yanovich
Licensed under the Eiffel Forum License 2.

This script aims to only display items that are searched for that are not currently installed on the current machine. This is originally designed to work only on Fedora 13.
"""
import os
import sys
import yum

def excluded_search():
    """
    Does a normal yum search, but excludes any packages that are already
    installed from the search results.
    """
    yb = yum.YumBase()
    yb.setCacheDir()
    
    pl = yb.doPackageLists()
    installed = [x.name for x in pl.installed]
    lopi = set(installed)

    search_terms = sys.argv[1:]
    search_list = ['name', 'summary', 'description', 'packager', 'group',
            'url']

    res = yb.searchGenerator(search_list, search_terms)
    res = sorted(res, key=lambda x: x[0])

    seen = set()
    results = []

    for (pkg, values) in res:
        if pkg.name not in seen and pkg.name not in installed:
            seen.add(pkg.name)
            results.append(pkg)

    return results

if __name__ == '__main__':

    print '%s Searching %s' % tuple(['-' * 30] * 2)
    for pkg in excluded_search():
        # Print name/summary
        print "%s : %s" % (pkg.name, pkg.summary)
