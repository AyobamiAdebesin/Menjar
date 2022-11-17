#!/usr/bin/env bash
# A bash script that generates the name of contributors to this project
set -e

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")/.."

{
	cat <<- 'EOH'
		# This file lists all individuals having contributed content
		# to the repository.
		# For how it is generated, see `hack/generate-authors.sh`.
	EOH
	echo
	git log --format='%aN <%aE>' | LC_ALL=C.UTF-8 sort -uf
} > AUTHORS	
