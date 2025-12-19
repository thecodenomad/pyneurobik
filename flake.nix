{
  description = "Neurobik CLI tool for downloading AI models and OCI images";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in {
      packages = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
        in rec {
          neurobik = python.pkgs.buildPythonPackage {
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

          default = neurobik;
        }
      );

      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
        in {
          default = pkgs.mkShell {
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
        }
      );
    };
}