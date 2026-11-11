#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build_dir="$(mktemp -d)"
trap 'rm -r -- "$build_dir"' EXIT

if command -v javac >/dev/null 2>&1; then
  compiler=(javac)
  compatibility=(--release 21)
else
  # Algunos entornos tienen el módulo JDK pero no el enlace ejecutable javac.
  compiler=(java com.sun.tools.javac.Main)
  # Ese JDK recortado puede carecer de ct.sym requerido por --release.
  compatibility=(-source 21 -target 21)
fi

"${compiler[@]}" "${compatibility[@]}" -d "$build_dir" \
  "$repo_dir/simulador-javafx/src/main/java/dev/marcosmoreira/aula/circuitos/Nand2Lesson.java" \
  "$repo_dir/simulador-javafx/src/test/java/dev/marcosmoreira/aula/circuitos/Nand2LessonSmoke.java" \
  "$repo_dir/simulador-javafx/src/main/java/dev/marcosmoreira/aula/interfaz/BoardRouting.java" \
  "$repo_dir/simulador-javafx/src/test/java/dev/marcosmoreira/aula/interfaz/BoardRoutingSmoke.java"
java -cp "$build_dir" dev.marcosmoreira.aula.circuitos.Nand2LessonSmoke
java -cp "$build_dir" dev.marcosmoreira.aula.interfaz.BoardRoutingSmoke
