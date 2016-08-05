#!/bin/bash
nslookup -type=any $1 > $2
nslookup -type=any $1
