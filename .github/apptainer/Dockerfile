## Apptainer that builds the release .sif files in apptainer-publish.yml: the official
## image, pinned by tag and digest. Dependabot (docker) proposes updates 14 days after each
## release. Upstream doesn't publish an image for every release (none for 1.5.0-1.5.4).
## SIFs use the default gzip compression, which older Apptainer and Singularity can read.
FROM ghcr.io/apptainer/apptainer:1.5.5@sha256:bf62d7cae28fe1ec3a728d64975fa738bc89bb073a1f085531e7a64ac959b1bc
