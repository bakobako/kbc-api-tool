from flask import render_template
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from src.update_config import get_config_json, update_configuration_json


class GetConfigForm(FlaskForm):
    config_url = StringField('Link to config that you want to change config parameters for',
                             validators=[DataRequired()])
    sapi_token = StringField('Storage API token', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateConfigForm(FlaskForm):
    config_url = StringField('Link to config that you want to change config parameters for',
                             validators=[DataRequired()])
    sapi_token = StringField('Storage API token', validators=[DataRequired()])
    config = TextAreaField('Configuration', render_kw={'class': 'form-control', 'rows': 20})
    submit_2 = SubmitField('Submit')


def update_configuration_using_forms():
    get_config_form = GetConfigForm()
    update_config_form = UpdateConfigForm()
    get_config_message = ""
    update_config_message = ""
    if get_config_form.submit.data and get_config_form.validate():
        config_url = get_config_form.config_url.data
        sapi_token = get_config_form.sapi_token.data
        try:
            config = get_config_json(config_url, sapi_token)
            update_config_form.config.data = json.dumps(config, indent=4)
            update_config_form.config_url.data = get_config_form.config_url.data
            update_config_form.sapi_token.data = get_config_form.sapi_token.data
        except Exception as exc:
            get_config_message = f"It failed because: {exc}"
            return render_template("/update-config/index.html",
                                   form=get_config_form,
                                   form_2=update_config_form,
                                   message=get_config_message,
                                   message_2=update_config_message)

    if update_config_form.submit_2.data and update_config_form.validate():
        config_url = update_config_form.config_url.data
        sapi_token = update_config_form.sapi_token.data
        config = update_config_form.config.data
        config = config.replace("\'", "\"")
        config = config.replace("False", "false")
        config = config.replace("True", "true")
        json_conf = json.loads(config.replace("\'", "\""))

        try:
            update_configuration_json(config_url, sapi_token, json_conf)
        except TypeError as exc:
            update_config_message = f"It failed because: {exc}"
            return render_template("/update-config/index.html",
                                   form=get_config_form,
                                   form_2=update_config_form,
                                   message=get_config_message,
                                   message_2=update_config_message)

    return render_template("/update-config/index.html",
                           form=get_config_form,
                           form_2=update_config_form,
                           message=get_config_message,
                           message_2=update_config_message)
