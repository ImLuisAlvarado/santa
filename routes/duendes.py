from flask import request, redirect
from entities.duende import Duende

def routes_duendes(app):
    @app.route('/duende', methods=['POST'])
    def save_duende():
        try:
            duende = Duende(nombre=request.form['nombre'],
                            especialidad=request.form['especialidad'])
        except ValueError as e:
            return str(e), 400
        duende.save()
        return redirect('/')

    @app.route('/duende/<int:id_duende>/asignar', methods=['POST'])
    def asignar_duende(id_duende):
        Duende.asignar(id_duende, request.form.get('id_carta'))
        return redirect('/')