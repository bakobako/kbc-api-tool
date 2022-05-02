from flask import render_template, Markup
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from src.update_config import get_config_json, update_configuration_json
from src.tool_v2 import run_debug_job, run_test_tag_job, get_state_json, update_state


class ToolGetConfigForm(FlaskForm):
    config_url = StringField('Link to Configuration ',
                             validators=[DataRequired()])
    sapi_token = PasswordField('Storage API token', validators=[DataRequired()])
    submit_get_config = SubmitField('Submit')


class ToolGetDebugJobForm(FlaskForm):
    run_debug_job_config_url = HiddenField('', validators=[DataRequired()])
    run_debug_job_sapi_token = HiddenField('', validators=[DataRequired()])
    submit_run_debug_job = SubmitField('Run Debug Job')


class ToolGetTestTagJobForm(FlaskForm):
    run_test_tag_job_config_url = HiddenField('', validators=[DataRequired()])
    run_test_tag_job_sapi_token = HiddenField('', validators=[DataRequired()])
    submit_run_test_tag_job = SubmitField('Run Test-Tag Job')


class ToolUpdateConfigForm(FlaskForm):
    update_config_url = HiddenField('',
                                    validators=[DataRequired()])
    update_sapi_token = HiddenField('', validators=[DataRequired()])
    config = TextAreaField('Configuration JSON (Edit and press update)',
                           render_kw={'class': 'form-control', 'rows': 20})
    submit_update_config = SubmitField('Update configuration')


class ToolUpdateStateForm(FlaskForm):
    update_state_url = HiddenField('',
                                   validators=[DataRequired()])
    update_state_sapi_token = HiddenField('', validators=[DataRequired()])
    state = TextAreaField('State JSON (Edit and press update)', render_kw={'class': 'form-control', 'rows': 20})
    submit_update_state = SubmitField('Update state')


def tool_update_configuration_using_forms():
    get_config_form = ToolGetConfigForm()
    update_config_form = ToolUpdateConfigForm()
    debug_job_form = ToolGetDebugJobForm()
    test_tag_job_form = ToolGetTestTagJobForm()
    update_state_form = ToolUpdateStateForm()
    get_config_message = ""
    update_config_message = ""

    forms = {
        "get_config_form": get_config_form,
        "update_config_form": update_config_form,
        "debug_job_form": debug_job_form,
        "test_tag_job_form": test_tag_job_form,
        "update_state_form": update_state_form,
        "message": get_config_message,
        "message_2": update_config_message
    }

    if forms["get_config_form"].submit_get_config.data and forms["get_config_form"].validate():
        config_url = forms["get_config_form"].config_url.data
        sapi_token = forms["get_config_form"].sapi_token.data
        try:
            config = get_config_json(config_url, sapi_token)
            state = get_state_json(config_url, sapi_token)

            forms["get_config_form"].config_url.data = config_url
            forms["get_config_form"].sapi_token.data = sapi_token

            forms["update_config_form"].update_config_url.data = get_config_form.config_url.data
            forms["update_config_form"].update_sapi_token.data = get_config_form.sapi_token.data

            forms["debug_job_form"].run_debug_job_config_url.data = get_config_form.config_url.data
            forms["debug_job_form"].run_debug_job_sapi_token.data = get_config_form.sapi_token.data

            forms["test_tag_job_form"].run_test_tag_job_config_url.data = get_config_form.config_url.data
            forms["test_tag_job_form"].run_test_tag_job_sapi_token.data = get_config_form.sapi_token.data

            forms["update_state_form"].update_state_url.data = get_config_form.config_url.data
            forms["update_state_form"].update_state_sapi_token.data = get_config_form.sapi_token.data

            forms["update_config_form"].config.data = json.dumps(config, indent=4)
            forms["update_state_form"].state.data = json.dumps(state, indent=4)
        except Exception as exc:
            print("fail")
            forms["message"] = Markup(
                f'<div class="col-xs-2"></div><div class="col-xs-10 error-box"><p class="errors"> It failed because: {exc}</p></div>')

            return render_template("/tool_v2/index.html", **forms)

    if forms["update_config_form"].submit_update_config.data and forms["update_config_form"].validate():
        config_url = forms["update_config_form"].update_config_url.data
        sapi_token = forms["update_config_form"].update_sapi_token.data

        forms["get_config_form"].config_url.data = config_url
        forms["get_config_form"].sapi_token.data = sapi_token

        forms["debug_job_form"].run_debug_job_config_url.data = config_url
        forms["debug_job_form"].run_debug_job_sapi_token.data = sapi_token

        forms["test_tag_job_form"].run_test_tag_job_config_url.data = config_url
        forms["test_tag_job_form"].run_test_tag_job_sapi_token.data = sapi_token

        state = get_state_json(config_url, sapi_token)
        forms["update_state_form"].update_state_url.data = get_config_form.config_url.data
        forms["update_state_form"].update_state_sapi_token.data = get_config_form.sapi_token.data
        forms["update_state_form"].state.data = json.dumps(state, indent=4)

        config = forms["update_config_form"].config.data
        config = config.replace("\'", "\"")
        config = config.replace("False", "false")
        config = config.replace("True", "true")
        try:
            json_conf = json.loads(config.replace("\'", "\""))
        except json.decoder.JSONDecodeError as exc:
            forms["message"] = Markup(
                f'<div class="col-xs-2"></div><div class="col-xs-10 error-box"><p>Error Updating Configuration</p><p class="errors"> JSON Decode error: {exc}</p></div>')
            return render_template("/tool_v2/index.html", **forms)

        try:
            update_configuration_json(config_url, sapi_token, json_conf)
        except Exception as exc:
            forms["message"] = Markup(
                f'<div class="col-xs-2"></div><div class="col-xs-10 error-box"><p>Error Updating Configuration</p><p class="errors"> Failed because: {exc}</p></div>')
            return render_template("/tool_v2/index.html", **forms)

    if forms["debug_job_form"].submit_run_debug_job.data and forms["debug_job_form"].validate():

        config_url = forms["debug_job_form"].run_debug_job_config_url.data
        sapi_token = forms["debug_job_form"].run_debug_job_sapi_token.data
        config = get_config_json(config_url, sapi_token)

        forms["get_config_form"].config_url.data = config_url
        forms["get_config_form"].sapi_token.data = sapi_token

        forms["update_config_form"].update_config_url.data = config_url
        forms["update_config_form"].update_config_url.data = sapi_token

        forms["test_tag_job_form"].run_test_tag_job_config_url.data = config_url
        forms["test_tag_job_form"].run_test_tag_job_sapi_token.data = sapi_token

        forms["update_config_form"].config.data = json.dumps(config, indent=4)

        state = get_state_json(config_url, sapi_token)
        forms["update_state_form"].update_state_url.data = get_config_form.config_url.data
        forms["update_state_form"].update_state_sapi_token.data = get_config_form.sapi_token.data
        forms["update_state_form"].state.data = json.dumps(state, indent=4)

        try:
            run_debug_job(config_url, sapi_token)
        except TypeError as exc:
            return render_template("/tool_v2/index.html", **forms)

    if forms["test_tag_job_form"].submit_run_test_tag_job.data and forms["test_tag_job_form"].validate():

        config_url = forms["test_tag_job_form"].run_test_tag_job_config_url.data
        sapi_token = forms["test_tag_job_form"].run_test_tag_job_sapi_token.data
        config = get_config_json(config_url, sapi_token)

        forms["get_config_form"].config_url.data = config_url
        forms["get_config_form"].sapi_token.data = sapi_token

        forms["update_config_form"].update_config_url.data = config_url
        forms["update_config_form"].update_config_url.data = sapi_token

        forms["debug_job_form"].run_debug_job_config_url.data = config_url
        forms["debug_job_form"].run_debug_job_sapi_token.data = sapi_token

        forms["update_config_form"].config.data = json.dumps(config, indent=4)

        state = get_state_json(config_url, sapi_token)
        forms["update_state_form"].update_state_url.data = get_config_form.config_url.data
        forms["update_state_form"].update_state_sapi_token.data = get_config_form.sapi_token.data
        forms["update_state_form"].state.data = json.dumps(state, indent=4)

        try:
            run_test_tag_job(config_url, sapi_token)
        except TypeError as exc:
            return render_template("/tool_v2/index.html", **forms)

    if forms["update_state_form"].submit_update_state.data and forms["update_state_form"].validate():

        config_url = forms["update_state_form"].update_state_url.data
        sapi_token = forms["update_state_form"].update_state_sapi_token.data
        config = get_config_json(config_url, sapi_token)

        forms["get_config_form"].config_url.data = config_url
        forms["get_config_form"].sapi_token.data = sapi_token

        forms["update_config_form"].update_config_url.data = config_url
        forms["update_config_form"].update_config_url.data = sapi_token
        forms["update_config_form"].config.data = json.dumps(config, indent=4)

        forms["debug_job_form"].run_debug_job_config_url.data = config_url
        forms["debug_job_form"].run_debug_job_sapi_token.data = sapi_token

        forms["test_tag_job_form"].run_test_tag_job_config_url.data = config_url
        forms["test_tag_job_form"].run_test_tag_job_sapi_token.data = sapi_token

        state = forms["update_state_form"].state.data
        state = state.replace("\'", "\"")
        state = state.replace("False", "false")
        state = state.replace("True", "true")

        try:
            json_state = json.loads(state.replace("\'", "\""))
        except json.decoder.JSONDecodeError as exc:
            forms["message"] = Markup(
                f'<div class="col-xs-2"></div><div class="col-xs-10 error-box"><p>Error Updating State</p><p class="errors"> JSON Decode error: {exc}</p></div>')
            return render_template("/tool_v2/index.html", **forms)

        try:
            update_state(config_url, sapi_token, json_state)
        except Exception as exc:
            forms["message"] = Markup(
                f'<div class="col-xs-2"></div><div class="col-xs-10 error-box"><p>Error Updating State</p><p class="errors"> Failed because: {exc}</p></div>')
            return render_template("/tool_v2/index.html", **forms)

    return render_template("/tool_v2/index.html", **forms)
