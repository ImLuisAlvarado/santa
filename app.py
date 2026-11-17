from flask import Flask

from routes.dashboard import routes_dashboard
from routes.ninos import routes_ninos
from routes.regalos import routes_regalos
from routes.cartas import routes_cartas
from routes.duendes import routes_duendes

app = Flask(__name__)

routes_dashboard(app)
routes_ninos(app)
routes_regalos(app)
routes_cartas(app)
routes_duendes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)