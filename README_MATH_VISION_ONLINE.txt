MATH VISION ONLINE - FIRST WEB VERSION
======================================

WHAT THIS PACKAGE IS
This is the first browser-based version of Math Vision. It is separate from, and does not replace, your working Tkinter/offline application.
Learners can visit the website, choose a generator, enter information, generate an SVG diagram, read its description, use browser speech, and download the SVG.

INCLUDED WEB GENERATORS
- Circle
- Pie Chart
- Bar Graph
- Set Theory Venn Diagram
- Bearing Diagram
- Scatter Graph
- Frequency Polygon
- Histogram
- Travel Graph
- Quadratic Graph
- Rectangle
- Triangle
- 3D Shapes and Nets (schematic starter nets)

IMPORTANT CONVERSION NOTE
The existing desktop generators use Tkinter. Tkinter windows cannot run inside a normal browser. This package reimplements the listed generators using a shared web-generator interface and SVG output. The original desktop files are not overwritten. Some complex desktop-specific controls and exact drawing layouts are not yet replicated; compare each web generator with the offline version and improve it in later iterations.

RUN LOCALLY ON WINDOWS
1. Extract the ZIP to a folder such as Documents\Math_Vision_Online.
2. Open Command Prompt in that folder.
3. Install the small Flask dependency:
   py -m pip install -r requirements.txt
4. Set an administrator password for this Windows session:
   set MATH_VISION_ADMIN_PASSWORD=Choose-A-Strong-Password
5. Start the website:
   py app.py
6. On the same computer, open http://127.0.0.1:5000 in a browser.

To stop the local server, return to Command Prompt and press Ctrl+C.

ADMINISTRATOR / ADDING GENERATORS
1. Set MATH_VISION_ADMIN_PASSWORD before starting the server.
2. Open /admin and sign in.
3. Upload a trusted .py plugin.
4. The main application scans web_generators automatically on each page request; no main application edit is needed.

PLUGIN CONTRACT
Each plugin must be a Python file in web_generators and define:
NAME = 'Friendly generator name'
DESCRIPTION = 'Short explanation'
FIELDS = [ {'name':'value','label':'Value','type':'text','default':'Example'} ]
def generate(values):
    return svg_string, plain_text_description

See circle.py, bearing.py and scatter_graph.py for examples. Plugins may use helper functions from common.py.

SECURITY - READ BEFORE PUTTING ONLINE
Uploaded Python files execute on the server. The upload page checks the required names and Python syntax, but this is NOT a security sandbox. Only upload code you personally wrote and reviewed. Do not let learners or unknown users upload plugins. Use a strong administrator password, set MATH_VISION_SECRET to a long random secret, use HTTPS, and deploy on a host that supports persistent storage. Before public launch, add stronger authentication, rate limits, backups, and a proper isolated plugin execution design.

DEPLOYMENT
This package is ready for local testing, not yet a public production deployment. Hosting providers have different requirements. A later deployment step must configure environment variables:
MATH_VISION_ADMIN_PASSWORD
MATH_VISION_SECRET
and run:
gunicorn app:app

The application currently binds to 127.0.0.1 for local safety. For a production host, change app.run host to 0.0.0.0 only if the host's instructions require it; normally the host will import app:app through its WSGI server.

ACCESSIBILITY
- Semantic headings and labels
- Keyboard-operable forms and buttons
- Skip-to-main-content link
- SVG title and description
- Plain text description
- Browser speechSynthesis where supported
- Downloadable SVG

EXAM INTEGRITY
Generators display supplied information. They do not intentionally calculate missing exam answers, statistical answers, reverse bearings, areas, perimeters, percentages or best-fit conclusions. The quadratic graph plots the entered expression as a visual graph; it does not list roots or turning points.
