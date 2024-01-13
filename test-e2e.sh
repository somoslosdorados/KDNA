#!/bin/bash

test_key_gen() {
  command="docker run -it kdna/e2e-client:latest poetry run python kdna/main.py encrypt key-gen"
  if $command; then
    echo "Tests key gen passed!"
  else
    echo "Tests key gen failed!"
  fi
}

test_create_tag(){
  command="poetry run python kdna/main.py tag add -p test -t test -f test.tar.gz -s S1"
  if $command; then
    echo "Tests create tag passed!"
  else
    echo "Tests create tag failed!"
  fi
}

run_tests() {
  test_key_gen
}

if [ $# == 2 ]; then
  if [ "$1" == "-i" ]; then
    echo "Running tests..."
    run_tests
  fi
else
  echo "Building image..."
  docker build -t kdna/e2e-client:latest .
  run_tests
fi


