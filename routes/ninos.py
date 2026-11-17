from flask import request, redirect
from entities.nino import Nino

def routes_ninos(app):
    @app.route('/nino', methods=['POST'])
    def save_nino():
        nino = Nino(nombre=request.form['nombre'],
                    direccion=request.form['direccion'],
                    pais=request.form['pais'],
                    puntos_comportamiento=request.form.get('puntos_comportamiento', 0))
        nino.save()
        return redirect('/')