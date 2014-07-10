#!/bin/sh
if [ -z "$2" ]; then
  echo "Usage: $0 SECONDS COMMAND" >&2
  exit 1
fi

SECONDS=$1
shift 1
while sleep $SECONDS; do
  clear
  $*
done
