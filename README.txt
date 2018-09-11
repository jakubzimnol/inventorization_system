This application is for inventorization products.
If you are logged you may check what products are in db, and send mail for admin to ask for take ownership of product.
If you are admin you may additionaly create, update, delete products.

For run application on Linux you must first install requirements, by getting into inventorization_system folder and pass in terminal:
pip install requirements.txt
After installing requirements install package "wkhtmltopdf" in ubuntu/debian
sudo apt-get install wkhtmltopdf
Next you must run server, you may do it by run local server by:
./manage.py runserver,
Then you may use this app in defined link.
