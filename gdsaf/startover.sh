cls
echo "rm -f db.sqlite3"
rm -f db.sqlite3
echo ""
echo ""
echo "python manage.py makemigrations"
python manage.py makemigrations
echo ""
echo ""
echo "python manage.py migrate"
python manage.py migrate
echo ""
echo ""
echo "python manage.py createsuperuser"
python manage.py createsuperuser
echo ""
echo ""
echo "python manage.py runserver"
python manage.py runserver
