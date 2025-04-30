#!/bin/bash

MODEL_DIR="$HOME/.cache/chroma/onnx_models/all-MiniLM-L6-v2"
MODEL_TAR_URL="https://huggingface.co/onnx/all-MiniLM-L6-v2/resolve/main/onnx.tar.gz"

# Crear directorio si no existe
mkdir -p "$MODEL_DIR"

# Descargar y descomprimir solo si no existe el modelo
if [ ! -f "$MODEL_DIR/model.onnx" ]; then
  echo "📦 Descargando modelo ONNX para Chroma..."
  curl -L "$MODEL_TAR_URL" -o "$MODEL_DIR/onnx.tar.gz"
  tar -xvzf "$MODEL_DIR/onnx.tar.gz" -C "$MODEL_DIR"
  rm "$MODEL_DIR/onnx.tar.gz"
  echo "✅ Modelo descargado y listo."
else
  echo "✅ Modelo ONNX ya presente en cache."
fi

