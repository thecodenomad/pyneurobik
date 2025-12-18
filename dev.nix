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
    # textual not in nixpkgs, will install via pip
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonWithPackages
  ];

  shellHook = ''
    echo "Neurobik development environment"
    export PYTHONPATH=$PWD:$PYTHONPATH
    # Create virtualenv and install textual
    python3 -m venv .venv
    source .venv/bin/activate
    pip install textual
  '';
}