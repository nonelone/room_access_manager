# Room Access Manager  
!["Project Icon"](https://raw.githubusercontent.com/nonelone/room_access_manager/master/static/icon.svg "Room Access Manager")  
RAM is a system for managing room access to rooms using NFC cards.  
I'm creating it as my bachelor's degree project.

Install dependencies using
`pip install -r requirements.txt`  
Generate secret using `secrets.token_hex(16)` and put it in `instance/secrets.py` as `SECRET_KEY` variable


Run the server using `python app.py`.  
On the first run, you will be prompted for user data for admin.  

`LICENCES.json` file contains licences of dependencies that are used in the program and was created using `pip-licenses`.


### Faker usage:
- Open python CLI in app folder  
- Import faker with `import fraud`
- Run `fraud.fake_admins(n)` where n is the number of fake admins  

You can also make fake users and locks with `fraud.fake_users(n)` and `fraud.fake_locks(n)` respectively.  
Fake admins will always have an email like `admin1@example.com` and password of `admin`.  
**Disclaimer:** You have to run the app at least once in order to initialize the database!


# TODO!

- user management page
- admin account creation
- adding locks
- managing permisions