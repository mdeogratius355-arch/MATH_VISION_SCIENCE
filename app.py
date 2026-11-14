
import os
import re
import ast
import uuid
import importlib.util
import sys

from pathlib import Path
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file,
    abort
)

app.logger.warning("MATH VISION ROOT: %s", ROOT)
app.logger.warning("TEMPLATE DIRECTORY: %s", TEMPLATE_DIR)
app.logger.warning("TEMPLATE DIRECTORY EXISTS: %s", TEMPLATE_DIR.exists())
app.logger.warning("TEMPLATE FILES FOUND: %s", [p.name for p in TEMPLATE_DIR.glob('*')])
ROOT = Path(__file__).resolve().parent

PLUGIN_DIR = ROOT / 'web_generators'
UPLOAD_DIR = ROOT / 'uploads'
TEMPLATE_DIR = ROOT / 'templates'
STATIC_DIR = ROOT / 'static'

PLUGIN_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
TEMPLATE_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

if str(PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGIN_DIR))

# Explicitly tell Flask where the website files are.
app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR)
)

app.secret_key = os.environ.get(
    'MATH_VISION_SECRET',
    'change-this-secret-before-deployment'
)

ADMIN_PASSWORD = os.environ.get(
    'MATH_VISION_ADMIN_PASSWORD',
    ''
)


# Automatically discover available diagram generators.
def discover_generators():
    found = []

    for path in sorted(PLUGIN_DIR.glob('*.py')):

        if path.name.startswith('_') or path.name == 'common.py':
            continue

        try:
            spec = importlib.util.spec_from_file_location(
                'mv_plugin_' + path.stem,
                path
            )

            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if not isinstance(getattr(mod, 'NAME', None), str):
                continue

            if not isinstance(getattr(mod, 'FIELDS', None), list):
                continue

            if not callable(getattr(mod, 'generate', None)):
                continue

            found.append((path.stem, mod))

        except Exception as exc:
            app.logger.warning(
                'Could not load generator %s: %s',
                path.name,
                exc
            )

    return found


# Administrator access protection.
def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        if not session.get('admin'):
            return redirect(url_for('admin_login'))

        return fn(*args, **kwargs)

    return wrapper


# Main homepage.
@app.route('/')
def home():

    return render_template(
        'index.html',
        generators=[
            (slug, mod.NAME, mod.DESCRIPTION)
            for slug, mod in discover_generators()
        ]
    )


# Diagram generator page.
@app.route('/generator/<slug>', methods=['GET', 'POST'])
def generator(slug):

    match = [
        (s, m)
        for s, m in discover_generators()
        if s == slug
    ]

    if not match:
        abort(404)

    _, mod = match[0]

    svg = None
    description = None
    error = None
    values = {}

    if request.method == 'POST':

        values = {
            field['name']: request.form.get(
                field['name'], ''
            ).strip()
            for field in mod.FIELDS
        }

        try:

            svg, description = mod.generate(values)

            if not isinstance(svg, str) or '<svg' not in svg[:500]:
                raise ValueError(
                    'Generator did not return a valid SVG diagram.'
                )

            session['last_svg'] = svg
            session['last_title'] = mod.NAME

        except Exception as exc:
            error = str(exc)

    return render_template(
        'generator.html',
        slug=slug,
        mod=mod,
        values=values,
        svg=svg,
        description=description,
        error=error
    )


# Download generated diagrams.
@app.route('/download')
def download():

    svg = session.get('last_svg')

    if not svg:
        abort(404)

    from flask import Response

    name = re.sub(
        r'[^a-z0-9_-]+',
        '_',
        session.get('last_title', 'math_vision').lower()
    )

    return Response(
        svg,
        mimetype='image/svg+xml',
        headers={
            'Content-Disposition':
            f'attachment; filename={name}.svg'
        }
    )


# Administrator login.
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():

    if not ADMIN_PASSWORD:
        return render_template(
            'admin_login.html',
            disabled=True
        )

    if request.method == 'POST':

        if request.form.get('password', '') == ADMIN_PASSWORD:

            session['admin'] = True

            return redirect(url_for('admin_dashboard'))

        flash('The password was not accepted.')

    return render_template(
        'admin_login.html',
        disabled=False
    )


# Administrator dashboard.
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():

    return render_template(
        'admin.html',
        generators=[
            (slug, mod.NAME, mod.DESCRIPTION)
            for slug, mod in discover_generators()
        ]
    )


# Upload new diagram generators.
@app.route('/admin/upload', methods=['POST'])
@admin_required
def admin_upload():

    file = request.files.get('plugin')

    if not file or not file.filename.lower().endswith('.py'):

        flash('Choose a Python generator file ending in .py.')

        return redirect(url_for('admin_dashboard'))

    filename = Path(file.filename).name

    if not re.fullmatch(
        r'[A-Za-z][A-Za-z0-9_-]{0,55}\.py',
        filename
    ):

        flash(
            'Use a simple filename with letters, numbers, underscores or hyphens.'
        )

        return redirect(url_for('admin_dashboard'))

    source = file.read(200_001)

    if len(source) > 200_000:

        flash('The file is too large (maximum 200 KB).')

        return redirect(url_for('admin_dashboard'))

    try:

        text = source.decode('utf-8')
        tree = ast.parse(text)

        top = {
            n.name
            for n in tree.body
            if isinstance(
                n,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef
                )
            )
        }

        assigns = {
            t.id
            for n in tree.body
            if isinstance(n, (ast.Assign, ast.AnnAssign))
            for t in (
                n.targets
                if isinstance(n, ast.Assign)
                else [n.target]
            )
            if isinstance(t, ast.Name)
        }

        if not {'NAME', 'DESCRIPTION', 'FIELDS'}.issubset(assigns):
            raise ValueError(
                'The generator must define NAME, DESCRIPTION, FIELDS and generate(values).'
            )

        if 'generate' not in top:
            raise ValueError(
                'The generator must define generate(values).'
            )

        compile(tree, filename, 'exec')

    except Exception as exc:

        flash('Generator validation failed: ' + str(exc))

        return redirect(url_for('admin_dashboard'))

    # Python plugins execute on the server.
    # Upload only code you wrote and trust.
    (PLUGIN_DIR / filename).write_text(
        text,
        encoding='utf-8'
    )

    flash(
        'Generator uploaded. It is now discovered by the main application. Test it before announcing it to learners.'
    )

    return redirect(url_for('admin_dashboard'))


# Administrator logout.
@app.route('/admin/logout')
def admin_logout():

    session.clear()

    return redirect(url_for('home'))


# Application health check.
@app.route('/health')
def health():

    return {
        'status': 'ok',
        'generators': len(discover_generators())
    }


# Run locally.
if __name__ == '__main__':

    app.run(
        host='127.0.0.1',
        port=int(os.environ.get('PORT', '5000')),
        debug=False
    )
