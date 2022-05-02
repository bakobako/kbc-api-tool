from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from src.tags import revert_tag


class RevertTagForm(FlaskForm):
    config_url = StringField('Link to config that you want to revert the tag for', validators=[DataRequired()])
    sapi_token = StringField('Storage API token', validators=[DataRequired()])
    submit = SubmitField('Submit')


def revert_tag_using_form():
    form = RevertTagForm()
    message = ""
    reverted = False
    if form.validate_on_submit():
        config_url = form.config_url.data
        sapi_token = form.sapi_token.data
        try:
            reverted = revert_tag(config_url, sapi_token)
        except Exception as exc:
            message = f"It failed because: {exc}"
            render_template("tags/revert_tag.html", form=form, message=message)
        if reverted:
            message = "Tag successfully changed"
        else:
            message = "It failed"
    return render_template("tags/revert_tag.html", form=form, message=message)
