# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  python-with-my-packages = pkgs.python310.withPackages (p: with p; [
    build
    setuptools
  ]);
in
python-with-my-packages.env
