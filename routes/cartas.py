from flask import request, redirect
from entities.carta import Carta

def routes_cartas(app):
    @app.route('/carta', methods=['POST'])
    def save_carta():
        carta = Carta(id_nino=request.form['id_nino'])
        carta.save()
        id_regalo = request.form.get('id_regalo')
        if id_regalo:
            try:
                carta.agregar_regalo(id_regalo, request.form.get('cantidad', 1))
            except ValueError as e:
                return str(e), 400
        return redirect('/')

    @app.route('/carta/<int:id_carta>/regalo', methods=['POST'])
    def add_regalo_a_carta(id_carta):
        carta = Carta(id_nino=request.form['id_nino'], id_carta=id_carta)
        try:
            carta.agregar_regalo(request.form['id_regalo'], request.form.get('cantidad', 1))
        except ValueError as e:
            return str(e), 400
        return redirect('/')

    @app.route('/carta/<int:id_carta>/estado', methods=['POST'])
    def update_estado(id_carta):
        try:
            Carta.actualizar_estado(id_carta, request.form['estado_preparacion'])
        except ValueError as e:
            return str(e), 400
        return redirect('/')