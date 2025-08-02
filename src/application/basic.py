from flask import Blueprint

basic_bp = Blueprint('health', __name__)

@basic_bp.route('/health')
def health():
    return 'ok'
