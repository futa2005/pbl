from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired


class LoginForm(FlaskForm):
    username = StringField('ユーザ名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class SignupForm(FlaskForm):
    username = StringField('ユーザ名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    confirm_password = PasswordField('パスワード確認', validators=[DataRequired(), EqualTo('password', message='パスワードが一致しません')])
    submit = SubmitField('アカウント登録')


class DeleteForm(FlaskForm):
    submit = SubmitField('削除')
    



class CreateForm(FlaskForm):
    title = StringField('あなたの味にただ一つの名前を', validators=[DataRequired(), Length(min=1, max=100)])
    body = TextAreaField('感想', validators=[DataRequired()])
    img = FileField('体験をシェア', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], '画像ファイルのみ許可されています。')])
    # アイコンカウント用の隠しフィールド
    icon1_count = HiddenField('Icon1 Count', default='0', render_kw={'id': 'hidden-icon1'})
    icon2_count = HiddenField('Icon2 Count', default='0', render_kw={'id': 'hidden-icon2'})
    icon3_count = HiddenField('Icon3 Count', default='0', render_kw={'id': 'hidden-icon3'})
    submit = SubmitField('ポストする')
    
    

class EditForm(FlaskForm):
    title = StringField('あなたの味にただ一つの名前を', validators=[DataRequired(), Length(min=1, max=100)])
    body = TextAreaField('感想', validators=[DataRequired()])
    img = FileField('体験をシェア')
    icon1_count = HiddenField('Icon1 Count', default='0', render_kw={'id': 'hidden-icon1'})
    icon2_count = HiddenField('Icon2 Count', default='0', render_kw={'id': 'hidden-icon2'})
    icon3_count = HiddenField('Icon3 Count', default='0', render_kw={'id': 'hidden-icon3'})
    submit = SubmitField('更新する')


