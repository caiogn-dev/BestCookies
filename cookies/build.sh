#!/bin/bash
set -e

# Instala dependências
pip install -r requirements.txt

# Aplica as migrações
python manage.py makemigrations
python manage.py migrate

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Mensagem de sucesso
echo "Build finalizado com sucesso! Pronto para deploy."
