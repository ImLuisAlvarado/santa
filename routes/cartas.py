from flask import request, redirect, render_template, url_for, flash
from entities.carta import Carta, ESTADOS
from entities.nino import Nino
from entities.regalo import Regalo


def routes_cartas(app):

    @app.route('/cartas')
    def lista_cartas():
        return render_template(
            'cartas.html',
            cartas=Carta.get_all(),
            ninos=Nino.get_all(),
            regalos=Regalo.get_all(),
            estados=ESTADOS,
        )

    @app.route('/cartas/<int:id_carta>')
    def detalle_carta(id_carta):
        carta = Carta.get_by_id(id_carta)
        if carta is None:
            flash('Carta no encontrada.', 'error')
            return redirect(url_for('lista_cartas'))
        return render_template(
            'detalle_carta.html',
            carta=carta,
            detalles=Carta.get_detalles(id_carta),
            regalos=Regalo.get_all(),
            estados=ESTADOS,
        )

    @app.route('/carta', methods=['POST'])
    def save_carta():
        carta = Carta(id_nino=request.form['id_nino'])
        carta.save()
        id_regalo = request.form.get('id_regalo')
        if id_regalo:
            try:
                carta.agregar_regalo(id_regalo, request.form.get('cantidad', 1))
                flash('Carta creada con éxito.', 'success')
            except ValueError as e:
                flash(str(e), 'error')
        else:
            flash('Carta creada con éxito.', 'success')
        return redirect(url_for('lista_cartas'))

    @app.route('/carta/<int:id_carta>/regalo', methods=['POST'])
    def add_regalo_a_carta(id_carta):
        carta_row = Carta.get_by_id(id_carta)
        if carta_row is None:
            flash('Carta no encontrada.', 'error')
            return redirect(url_for('lista_cartas'))
        carta = Carta(id_nino=carta_row['id_nino'], id_carta=id_carta)
        try:
            carta.agregar_regalo(request.form['id_regalo'], request.form.get('cantidad', 1))
            flash('Regalo agregado.', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        return redirect(url_for('detalle_carta', id_carta=id_carta))

    @app.route('/carta/<int:id_carta>/estado', methods=['POST'])
    def update_estado(id_carta):
        try:
            Carta.actualizar_estado(id_carta, request.form['estado_preparacion'])
            flash('Estado actualizado.', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        referer = request.referrer or ''
        if f'/cartas/{id_carta}' in referer:
            return redirect(url_for('detalle_carta', id_carta=id_carta))
        return redirect(url_for('lista_cartas'))

    @app.route('/carta/<int:id_carta>/regalo/<int:id_detalle>/eliminar', methods=['POST'])
    def eliminar_regalo_de_carta(id_carta, id_detalle):
        Carta.eliminar_regalo(id_detalle)
        flash('Regalo eliminado de la carta.', 'success')
        return redirect(url_for('detalle_carta', id_carta=id_carta))

    @app.route('/carta/<int:id_carta>/eliminar', methods=['POST'])
    def eliminar_carta(id_carta):
        Carta.delete(id_carta)
        flash('Carta eliminada.', 'success')
        return redirect(url_for('lista_cartas'))
