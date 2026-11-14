from flask import Flask, render_template, request, redirect

from entities.nino import Nino
from entities.regalo import Regalo
from entities.carta import Carta, ESTADOS
from entities.duende import Duende, ESPECIALIDADES

app = Flask(__name__)


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


@app.route('/nino', methods=['POST'])
def save_nino():
    nino = Nino(nombre=request.form['nombre'],
                direccion=request.form['direccion'],
                pais=request.form['pais'],
                puntos_comportamiento=request.form.get('puntos_comportamiento', 0))
    nino.save()
    return redirect('/')


@app.route('/regalo', methods=['POST'])
def save_regalo():
    regalo = Regalo(nombre=request.form['nombre'],
                    descripcion=request.form.get('descripcion', ''),
                    categoria_juguete=request.form['categoria_juguete'],
                    puntos_comportamiento_requeridos=request.form.get(
                        'puntos_comportamiento_requeridos', 0))
    regalo.save()
    return redirect('/')


@app.route('/carta', methods=['POST'])
def save_carta():
    """Crea una carta y, opcionalmente, su primer regalo."""
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
