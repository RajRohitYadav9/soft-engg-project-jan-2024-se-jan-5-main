#! /bin/sh
echo "Welcome to the setup." 
echo "This will activate the local virtual env and run the required python files."
echo "You can rerun this without any issues."

if [ -d ".venv" ];
then
    echo "Enabling virtual env"
else
    echo "No virtual venv. Please run 'local_setup.sh' first"
    exit N
fi

# Activate virtual env
. .venv/Scripts/activate

export ENV=development
cd backend
celery -A application.tasks.celery beat --max-interval 1 -l info
deactivate