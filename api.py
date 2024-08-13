from flask import Blueprint, abort, request
from models import Tokens, Lock, db

api_blueprint = Blueprint('api', __name__)

def check_authority(nfc_id, lock_id):
    token = db.session.query(Tokens).join(Lock).filter(
        Tokens.nfc_id == nfc_id,
        Tokens.lock_id == lock_id
    ).first()
    return token is not None

@api_blueprint.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        token = request.form['token']
        card_id = request.form['card_id']
        print(token, card_id)
        if token is None or card_id is None: abort(403)

        lock = Lock.query.filter_by(token=token).first()
        if lock is None: abort(403)
        lock_id = lock.id
        
        if check_authority(card_id, lock_id):
            return 'Authorized'
        else:
            abort(403)
    
    elif request.method == 'GET':
        return '<title>API</title><h1>For API usage, dummy!</h1>'
    abort(403)