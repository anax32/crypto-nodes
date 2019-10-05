#!/bin/sh
set -u

LABEL=$1
INPUT=$2

COUNT=$(awk -v label="$LABEL" '$2 == label' "$INPUT" | wc -l)

echo "$LABEL $COUNT"
