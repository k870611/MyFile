from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired

from app.models import User, Role


class LoginForm(FlaskForm):
    userName = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class AccountCreateForm(FlaskForm):
    account = StringField('account', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    cellphone = StringField('cellphone')
    active = BooleanField('active')
    deadlineChk = BooleanField('deadlineChk')
    deadlineFrom = StringField('deadlineFrom')
    deadlineTo = StringField('deadlineTo')
    organization = StringField('organization')
    orgManager = BooleanField('orgManager Manager')

    @staticmethod
    def validate_account(self, account):
        if str(account.data).find(',') >= 0:
            raise ValidationError("Account cannot contain ',' ")
        user = User.query.filter_by(acc_management_account=account.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(acc_management_email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AccountModifyForm(FlaskForm):
    account = StringField('account', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    cellphone = StringField('cellphone')
    active = BooleanField('active')
    deadlineChk = BooleanField('deadlineChk')
    deadlineFrom = StringField('deadlineFrom')
    deadlineTo = StringField('deadlineTo')
    organization = StringField('organization')
    originalAccount = StringField('originalAccount')
    originalEmail = StringField('originalEmail')

    # @staticmethod
    def validate_account(self, account):
        if str(account.data).find(',') >= 0:
            raise ValidationError("Account cannot contain ',' ")

        user = User.query.filter_by(acc_management_account=account.data).first()
        if user is not None and (user.acc_management_account != self.originalAccount.data):
            raise ValidationError('Please use a different username')

    # @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(acc_management_email=email.data).first()
        if user is not None and (user.acc_management_email != self.originalEmail.data):
            raise ValidationError('Please use a different email address')


class RoleModifyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    originalRole = StringField('originalRole')

    # @staticmethod
    def validate_name(self, name):
        role = Role.query.filter_by(role_name=name.data).first()
        if role is not None and (role.role_name != self.originalRole.data):
            raise ValidationError('Please use a different role name')