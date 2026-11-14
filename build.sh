#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Retrain crop model to ensure pickle compatibility with deployed sklearn version
python -c "from ml_models.train_crop_model import train_and_evaluate; train_and_evaluate()"

python manage.py collectstatic --noinput
python manage.py migrate
