from flask import render_template
from entities.nino import Nino
from entities.regalo import Regalo
from entities.carta import Carta, ESTADOS
from entities.duende import Duende, ESPECIALIDADES

def routes_dashboard(app):
    @app.route('/')
    def index():
        return render_template(
            'index.html',
            ninos=Nino.get_all(),
            regalos=Regalo.get_all(),
            cartas=Carta.get_all(),
            duendes=Duende.get_all(),
            estados=ESTADOS,
            especialidades=ESPECIALIDADES,
        )