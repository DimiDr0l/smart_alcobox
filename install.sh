#!/bin/bash
set -e

apt update && apt upgrade
apt install python3-dev ffmpeg vim portaudio19-dev alsa-base alsa-utils -y
