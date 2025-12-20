{ pkgs ? import <nixpkgs> {} }:

let
  pythonWithPackages = pkgs.python3.withPackages (ps: with ps; [
    pip
    requests
    tqdm
    pyyaml
    click
    pydantic
    loguru
    pytest
    pytest-cov
    questionary
    huggingface-hub
    black
    pylint
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonWithPackages
  ];

  shellHook = ''
    echo "Neurobik development environment"
    export PYTHONPATH=$PWD:$PYTHONPATH
  '';
}