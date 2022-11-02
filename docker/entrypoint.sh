#!/bin/bash
. /etc/.bashrc

# # Run CMD
# /bin/bash "$@"

echo "$@"
exec "$@"
