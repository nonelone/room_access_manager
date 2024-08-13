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

        lock_id = Lock.query.filter_by(token=token).first().id
        print(lock_id)
        if lock_id is None: abort(403)

        connected = db.session.query(Tokens).filter(Tokens.nfc_id == card_id).filter(Tokens.lock_id == lock_id).all()
        print(connected)
        #allowed_tokens = Tokens.query.with_entities(Tokens.token_id).all()
        #avaliable_locks = Tokens.query.filter(Lock.id == lock_id).all()
        #allowed_token_ids = [token[0] for token in allowed_tokens]
        #abort(503)
        
        #if token not in allowed_token_ids:
        #    abort(403)
        if check_authority(card_id, lock_id):
            return 'Authorized'
        else:
            abort(403)
    
    elif request.method == 'GET':
        return '<title>API</title><h1>For API usage, dummy!</h1>'
    abort(403)