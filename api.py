from flask import Blueprint, abort, request
from models import Tokens, Lock, db

api_blueprint = Blueprint('api', __name__)

def check_authority(nfc_id, token_id):
    token = db.session.query(Tokens).join(Lock).filter(
        Tokens.nfc_id == nfc_id,
        Tokens.token_id == token_id
    ).first()
    return token is not None

@api_blueprint.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        token = request.form['token']
        card_id = request.form['card_id']
        print(token, card_id)
        if token is None or card_id is None: abort(403)

        allowed_tokens = Tokens.query.with_entities(Tokens.token_id).all()
        allowed_token_ids = [token[0] for token in allowed_tokens]
        
        if int(token) not in allowed_token_ids:
            abort(403)
        if check_authority(int(card_id), int(token)):
            return 'Authorized'
    
    elif request.method == 'GET':
        return '<title>API</title><h1>For API usage, dummy!</h1>'
    abort(403)