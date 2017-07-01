#!/bin/bash

if [ ! -z "$TRAVIS_TAG" ]; then
	flit publish
	echo "Published version $TRAVIS_TAG to PyPi"
else
	echo "nothing to publish"
fi
