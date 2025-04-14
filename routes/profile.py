import os
from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from forms.profile_form import ProfileEditForm
from extensions import db
from models.user import User

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


# Fallback Route
@profile_bp.route('/profile')
@login_required
def my_profile():
    return redirect(url_for('profile.view_profile', username=current_user.username))


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm()  # Use ProfileEditForm for editing bio and profile picture
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        if form.profile_picture.data:
            # Save the profile picture if it was uploaded
            picture = form.profile_picture.data
            picture_filename = secure_filename(picture.filename)

            # Ensure the upload folder is set and exists
            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])


            picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_filename)
            picture.save(picture_path)
            current_user.profile_picture = picture_filename  # Store the filename in the user's profile
        

        # Handle cover photo upload
        # if form.cover_photo.data:
        #     cover_picture = form.cover_photo.data
        #     cover_filename = secure_filename(cover_picture.filename)
        #     cover_path = os.path.join(current_app.config['UPLOAD_FOLDER'], cover_filename)
        #     cover_picture.save(cover_path)
        #     current_user.cover_photo = cover_filename  # Store the filename in the user's cover photo


        db.session.commit()
        return redirect(url_for('profile.view_profile'))

    form.bio.data = current_user.bio
    return render_template('edit_profile.html', form=form)

@profile_bp.route('/<username>', methods=['GET'])
@login_required
def view_profile(username):
    # Fetch the user by username
    user = User.query.filter_by(username=username).first_or_404()

    # Ensure users can only view their own profile or public profiles
    if not user:
        abort(404)

    return render_template('view_profile.html', user=user, current_user=current_user)
