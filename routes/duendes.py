from flask import request, redirect, render_template
from entities.duende import Duende, ESPECIALIDADES


def routes_duendes(app):
    @app.route('/duendes')
    def list_duendes():
        return render_template('duendes.html',
                               duendes=Duende.get_all(),
                               cartas=Duende.cartas_pendientes(),
                               especialidades=ESPECIALIDADES)

    @app.route('/duende', methods=['POST'])
    def save_duende():
        try:
            duende = Duende(nombre=request.form['nombre'],
                            especialidad=request.form['especialidad'])
        except ValueError as e:
            return str(e), 400
        duende.save()
        return redirect('/duendes')

    @app.route('/duende/<int:id_duende>/asignar', methods=['POST'])
    def asignar_duende(id_duende):
        try:
            Duende.asignar(id_duende, request.form.get('id_carta'))
        except ValueError as e:
            return str(e), 400
        return redirect('/duendes')