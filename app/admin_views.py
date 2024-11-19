from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, session, flash
from app.auth.models import Admin

class AdminModelView(ModelView):
    def is_accessible(self):
        # Перевіряємо, чи користувач є адміністратором
        user_id = session.get('user_id')
        if not user_id:
            return False

        # Перевірка наявності запису в таблиці admins
        return Admin.query.filter_by(user_id=user_id).first() is not None

    def inaccessible_callback(self, name, **kwargs):
        # Якщо доступ заборонений, перенаправляємо на головну сторінку
        flash("You don't have access to this page.", "danger")
        return redirect(url_for('main.index'))
