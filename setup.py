#!/usr/bin/env python

from setuptools import setup
import os

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "dfs",
  version = "0.0.1",
  author = "Dennis Blommesteijn",
  author_email = "dennis@blommesteijn.com",
  description = ("dfs"),
  license = "MIT",
  keywords = "dfs object-store file-system",
  url = "https://github.com/dblommesteijn/dfs",
  packages = ['dfs'],
  package_dir = {'dfs': "src/"} ,
  long_description = read('README.md'),
  scripts = ["scripts/dfs"],
  install_requires = [
    "distribute", 'Flask', 'Flask-Script', 'Flask-Jsonpify'
  ]
)