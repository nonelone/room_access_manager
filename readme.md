# Room Access Manager  
!["Project Icon"](https://raw.githubusercontent.com/nonelone/room_access_manager/master/icon.svg "Room Access Manager")  
RAM is a system for managing room access to rooms using NFC cards.  
I'm creating it as my bachelor's degree project.

Install dependencies using
`pip install -r requirements.txt`  
Generate secret using `secrets.token_hex(16)` and put it in `instance/secrets.py` as `SECRET_KEY` variable


Run the server using `python app.py`.  
On the first run, you will be prompted for user data for admin.  

`LICENCES.json` file contains licences of dependencies that are used in the program and was created using `pip-licenses`.
