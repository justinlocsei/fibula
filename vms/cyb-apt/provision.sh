#!/bin/bash

fib deploy bootstrap apt --inventory=development --user=vagrant --playbook=repo.yml --force "$@"
