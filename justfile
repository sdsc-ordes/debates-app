set positional-arguments
set shell := ["bash", "-cue"]
comp_dir := justfile_directory()
root_dir := `git rev-parse --show-toplevel`

container-mgr := "docker"

start:
  #!/usr/bin/env bash
  cd "{{root_dir}}" &&
  "{{container-mgr}}-compose" -d up &&
  "{{container-mgr}}-compose" exec solr bash ~/load-data.sh

