#!/bin/sh
set -eu

theme_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
symbols="$theme_dir/../../sddm/aura-soulflame/AuraSymbols.otf"
font_dir=${1:-$theme_dir}
range=0x20-0x24f,0x2000-0x219f,0x2500-0x257f,0xe9a0-0xe9a2

build_font() {
    source_font=$(fc-match -f '%{file}' "$1:style=Regular")
    grub-mkfont -n "$2" -s "$3" -r "$range" -o "$font_dir/$4.pf2" "$source_font" "$symbols"
}

mkdir -p "$font_dir"
build_font 'Noto Serif' 'Aura Title' 40 title40
build_font 'Noto Sans' 'Aura Item' 22 item22
build_font 'Noto Sans' 'Aura Small' 16 small16
build_font 'Noto Sans Mono' 'Aura Mono' 16 mono16
