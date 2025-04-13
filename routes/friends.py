import os
from flask import Blueprint, render_template, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.friendship import Friendship

# Blueprint
friends_bp = Blueprint('friends', __name__)


# View Friends List
@friends_bp.route('/friends')
@login_required
def friends():
    friends = Friendship.query.filter(
        ((Friendship.user_id == current_user.id) & (Friendship.status == 'accepted')) | 
        ((Friendship.friend_id == current_user.id) & (Friendship.status == 'accepted'))
    ).all()

    friend_list = []
    for friendship in friends:
        if friendship.user_id == current_user.id:
            friend_list.append(friendship.friend)
        else:
            friend_list.append(friendship.user)
    
    return render_template('friends.html', friends=friend_list)


# Send a Friend Request
@friends_bp.route('/send_friend_request/<int:friend_id>', methods=['POST'])
@login_required
def send_friend_request(friend_id):
    friend = User.query.get_or_404(friend_id)

    # Check if the users are already friends or if the request is already sent
    existing_friendship = Friendship.query.filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == current_user.id))
    ).first()

    if existing_friendship:
        flash("You are already friends or have a pending request.", "info")
    else:
        new_request = Friendship(user_id=current_user.id, friend_id=friend_id, status='pending')
        db.session.add(new_request)
        db.session.commit()
        flash("Friend request sent!", "Success")

    return redirect(url_for('profile', username=friend.username))  # Redirect to the friend's profile


# Accept a Friend Request
@friends_bp.route('/accept_friend_request/<int:friendship_id>', methods=['POST'])
@login_required
def accept_friend_request(friendship_id):
    friendship = Friendship.query.get_or_404(friendship_id)

    if friendship.friend_id == current_user.id and friendship.status == 'pending':
        friendship.status = 'accepted'
        db.session.commit()
        flash("Friend request accepted!", "Success")
    else:
        flash("Invalid friend request.")

    return redirect(url_for('profile', username=current_user.username))


# Delete a Friend Request
@friends_bp.route('/reject_friend_request/<int:friendship_id>', methods=['POST'])
@login_required
def reject_friend_request(friendship_id):
    friendship = Friendship.query.get_or_404(friendship_id)

    if friendship and friendship.friend_id == current_user.id and friendship.status == 'pending':
        db.session.delete(friendship)
        db.session.commit()
        flash("Friend request rejected.")
    else:
        flash("Invalid friend request.")

    return redirect(url_for('profile', username=current_user.username))
