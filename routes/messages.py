from flask import Blueprint, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.message import Message
from extensions import db
# from app import app

# Blueprint
messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    if message.receiver_id != current_user.id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Unauthorized'}), 403
        flash('You are not authorized to delete this message.', 'danger')
        return redirect(url_for('profile.inbox'))

    db.session.delete(message)
    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True}), 200

    flash('Message deleted.', 'success')
    return redirect(url_for('profile.inbox'))
