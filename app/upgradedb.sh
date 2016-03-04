if [ -d "./migrations" ]; then
	rm -rf "./migrations"
fi
python models.py db init
python models.py db migrate
python models.py db upgrade

