from flask import request, redirect
from entities.regalo import Regalo

def routes_regalos(app):
    @app.route('/regalo', methods=['POST'])
    def save_regalo():
        regalo = Regalo(nombre=request.form['nombre'],
                        descripcion=request.form.get('descripcion', ''),
                        categoria_juguete=request.form['categoria_juguete'],
                        puntos_comportamiento_requeridos=request.form.get(
                            'puntos_comportamiento_requeridos', 0))
        regalo.save()
        return redirect('/')