{
  description = "Neurobik CLI tool for downloading AI models and OCI images";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";  # Adjust for your system
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3;
    in {
      packages.${system}.neurobik = python.pkgs.buildPythonPackage {
        pname = "neurobik";
        version = "0.1.0";
        src = ./.;
        format = "pyproject";

        nativeBuildInputs = with python.pkgs; [
          setuptools
          wheel
        ];

        propagatedBuildInputs = with python.pkgs; [
          requests
          tqdm
          pyyaml
          click
          pydantic
          loguru
          questionary
        ];

        meta = {
          description = "CLI tool for downloading AI models and OCI images";
          license = pkgs.lib.licenses.gpl3;
        };
      };

      packages.${system}.default = self.packages.${system}.neurobik;

      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          python
          python.pkgs.pip
          python.pkgs.requests
          python.pkgs.tqdm
          python.pkgs.pyyaml
          python.pkgs.click
          python.pkgs.pydantic
          python.pkgs.loguru
          python.pkgs.questionary
        ];

        shellHook = ''
          echo "Neurobik development environment"
          export PYTHONPATH=$PWD:$PYTHONPATH
        '';
      };
    };
}