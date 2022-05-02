from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from src import update_configuration_using_forms, revert_tag_using_form, change_tag_using_form, \
    tool_update_configuration_using_forms
from flask import send_from_directory
import os

app = Flask(__name__, static_folder='static')
# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


# all Flask routes below

# two decorators using the same function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return tool_update_configuration_using_forms()


@app.route('/tags/index.html', methods=['GET', 'POST'])
def tag():
    return render_template("tags/index.html")


@app.route('/tags/change_tag.html', methods=['GET', 'POST'])
def change_tag_to_new():
    return change_tag_using_form()


@app.route('/tags/revert_tag.html', methods=['GET', 'POST'])
def revert_tag_to_default():
    return revert_tag_using_form()


@app.route('/update-config/index.html', methods=['GET', 'POST'])
def update_config():
    return update_configuration_using_forms()


@app.route('/tool/index.html', methods=['GET', 'POST'])
def new_tool():
    return tool_update_configuration_using_forms()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# keep this as is
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
