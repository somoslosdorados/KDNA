#!/bin/bash

command=""

build_command(){
  command="docker run --network kdna-e2e -it kdna/e2e-client:latest poetry run $1"
}

add_command(){
  command="$command && $1"
}

test_key_gen() {
  echo "Testing key gen..."
  build_command "python kdna/__main__.main encrypt key-gen"
  if $command; then
    echo "Tests key gen passed!"
  else
    echo "Tests key gen failed!"
  fi
}

test_create_project(){
  build_command "python kdna/main.py server add -i S1 -ad test@e2e-server -a jul -r test -p 2"
  build_command "ls"
  docker run --network kdna-e2e -it kdna/e2e-client:latest ssh test@e2e-server "ls"
  if $command; then
    echo "Tests create project passed!"
  else
    echo "Tests create project failed!"
  fi
}

test_create_tag(){
  build_command "python kdna/__main__.py encrypt create-tag --tag-name test --tag-value test"
  if $command; then
    echo "Tests create tag passed!"
  else
    echo "Tests create tag failed!"
  fi
}

run_tests() {
  echo "Running tests..."
  test_key_gen
  test_create_project
}

echo "$#"
if [ $# == 1 ]; then
  if [ "$1" == "-i" ]; then
    run_tests
  fi
else
  echo "Building image..."
  docker build -t kdna/e2e-client:latest .
  run_tests
fi
