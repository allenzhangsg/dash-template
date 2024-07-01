if [ "$DEPLOYENV" = "Production" ]; then
    echo "Running in $DEPLOYENV env."
    celery -A app:celery_app worker -l INFO -c 2 -Q production | tee /dev/null &
elif [ "$DEPLOYENV" = "Dev" ]; then
    echo "Running in $DEPLOYENV env."
    celery -A app:celery_app worker -l INFO -c 2  -Q dev | tee /dev/null &
else
    echo "Running at local. No celery workers to start"
fi
gunicorn app:flask_app -c ./gunicorn.conf.py | tee /dev/null &
wait