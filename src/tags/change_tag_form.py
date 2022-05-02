from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from src.tags import change_tag


class ChangeTagForm(FlaskForm):
    config_url = StringField('Link to config that you want to change the tag for', validators=[DataRequired()])
    sapi_token = StringField('Storage API token', validators=[DataRequired()])
    new_tag_name = StringField('Name of tag', validators=[DataRequired()], default="test")
    submit = SubmitField('Submit')


def change_tag_using_form():
    form = ChangeTagForm()
    message = ""
    if form.validate_on_submit():
        config_url = form.config_url.data
        sapi_token = form.sapi_token.data
        new_tag_name = form.new_tag_name.data
        try:
            changed = change_tag(config_url, sapi_token, new_tag_name)
        except Exception as exc:
            message = f"It failed because: {exc}"
            return render_template("tags/change_tag.html", form=form, message=message)
        if changed:
            message = "Tag successfully changed"
        else:
            message = "It failed"
    return render_template("tags/change_tag.html", form=form, message=message)
