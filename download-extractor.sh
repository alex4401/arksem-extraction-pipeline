#!/bin/bash
PROJECT_ID=13304753
PROJECT_BRANCH=$1
OUTPUT_FILENAME=$2

error_wusage() {
    echo "error: $@"
    echo "usage: bash $0 \$PROJECT_BRANCH \$OUTPUT_FILENAME"
    exit 1
}

[ -z "$PROJECT_BRANCH" ] \
    && error_wusage "Extractor branch has not been specified."
[ -z "$OUTPUT_FILENAME" ] \
    && error_wusage "Output filename has not been specified."

GITLAB_API="https://gitlab.com/api/v4/projects"
ARTIFACTS="jobs/artifacts"

FULL_URL="$GITLAB_API/$PROJECT_ID/$ARTIFACTS/$PROJECT_BRANCH/raw/target/debug/uasset-data-extractor?job=build"
echo "(downloading an artifact: $FULL_URL)"
exec curl "$FULL_URL" --output "$OUTPUT_FILENAME"