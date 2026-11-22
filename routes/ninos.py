from flask import request, redirect, render_template, url_for
from entities.nino import Nino

def routes_ninos(app):
    @app.route("/ninos/nuevo", methods=["GET", "POST"])
    def save_nino():
        if request.method == "POST":
            try:
                nino = Nino(
                    nombre=request.form.get("nombre", ""),
                    direccion=request.form.get("direccion", ""),
                    pais=request.form.get("pais", ""),
                    puntos_comportamiento=request.form.get("puntos_comportamiento", 0),
                )
                nino.save()
                return redirect(url_for("list_ninos"))
            except ValueError as e:
                return render_template("nino_form.html", nino=None, error=str(e)), 400

        return render_template("nino_form.html", nino=None, error=None)
    
    @app.route("/ninos", methods=["GET"])
    def list_ninos():
        ninos = Nino.get_all()
        return render_template("ninos.html", ninos=ninos)

    @app.route("/ninos/editar/<int:id_nino>", methods=["GET", "POST"])
    def edit_nino(id_nino):
        nino_actual = Nino.get_by_id(id_nino)
        if not nino_actual:
            return redirect(url_for("list_ninos"))

        if request.method == "POST":
            try:
                nino = Nino(
                    id_nino=id_nino,
                    nombre=request.form.get("nombre", ""),
                    direccion=request.form.get("direccion", ""),
                    pais=request.form.get("pais", ""),
                    puntos_comportamiento=request.form.get("puntos_comportamiento", 0),
                )
                nino.update()
                return redirect(url_for("list_ninos"))
            except ValueError as e:
                return (
                    render_template("nino_form.html", nino=nino_actual, error=str(e)),
                    400,
                )

        return render_template("nino_form.html", nino=nino_actual, error=None)

    @app.route("/ninos/eliminar/<int:id_nino>", methods=["POST"])
    def delete_nino(id_nino):
        Nino.delete(id_nino)
        return redirect(url_for("list_ninos"))