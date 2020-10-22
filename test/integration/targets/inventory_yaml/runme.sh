#!/usr/bin/env bash

# handle empty/commented out group keys correctly https://github.com/assible/assible/issues/47254
ASSIBLE_VERBOSITY=0 diff -w <(assible-inventory -i ./test.yml --list) success.json
