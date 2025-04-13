from extensions import db

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')

    user = db.relationship('User', foreign_keys=[user_id], backref='sent_requests')
    friend = db.relationship('User', foreign_keys=[friend_id], backref='received_requests')

    def __repr__(self):
        return f'<Friendship {self.user.username} and {self.friend.username} - {self.status}>'