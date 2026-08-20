import flet as ft
from datetime import datetime
import json
import random


def main(page: ft.Page):
    page.title = "Marcador de la EBDV"
    page.bgcolor = "#0f0f11"
    page.padding = 15
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 760
    page.window.resizable = False

    # --- Estado Inicial ---
    def init_state():
        return {
            "diaActual": 1,
            "desbloqueadoHasta": 1,
            "torneoFinalizado": False,
            "ocultarDia5": False,
            "dias": {str(i): {"rojo": 0, "azul": 0, "historial": []} for i in range(1, 6)}
        }

    state = init_state()

    # Cargar datos persistentes (ClientStorage de Flet)
    try:
        raw = page.client_storage.get("marcador_state_py")
        if raw:
            loaded = json.loads(raw)
            if "dias" in loaded and "1" in loaded["dias"]:
                state = loaded
    except Exception:
        state = init_state()

    def guardar_estado():
        try:
            page.client_storage.set("marcador_state_py", json.dumps(state))
        except Exception:
            pass
        render()

    def formatear_numero(num):
        num = int(num)
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M".replace(".0M", "M")
        if num >= 10_000:
            return f"{num / 1_000:.1f}k".replace(".0k", "k")
        return f"{num:,}".replace(",", ".")

    # --- Elementos Visuales del Marcador ---
    score_rojo = ft.Text("0", size=48, weight=ft.FontWeight.BOLD, color="#ff5252")
    score_azul = ft.Text("0", size=48, weight=ft.FontWeight.BOLD, color="#448aff")
    divider_text = ft.Text("-", size=32, weight=ft.FontWeight.W_300, color="#333338")

    total_rojo = ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color="#ff5252")
    total_azul = ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color="#448aff")

    titulo_historial = ft.Text("Registro Día 1", size=12, color="#666670", weight=ft.FontWeight.BOLD)
    total_registros = ft.Text("0 anotaciones", size=12, color="#666670")
    lista_historial = ft.ListView(spacing=8, height=130)

    # --- Acciones de Puntuación ---
    def modificar_puntos(equipo, cantidad):
        dia_str = str(state["diaActual"])
        dia_data = state["dias"][dia_str]
        hora = datetime.now().strftime("%H:%M")

        if equipo == "rojo":
            if dia_data["rojo"] + cantidad >= 0:
                dia_data["rojo"] += cantidad
                accion = "Punto" if cantidad > 0 else "Descuento"
                marcador_str = f"{formatear_numero(dia_data['rojo'])} - {formatear_numero(dia_data['azul'])}"
                dia_data["historial"].insert(0, {"equipo": "Rojo", "accion": accion, "hora": hora,
                                                 "marcador": marcador_str})
        elif equipo == "azul":
            if dia_data["azul"] + cantidad >= 0:
                dia_data["azul"] += cantidad
                accion = "Punto" if cantidad > 0 else "Descuento"
                marcador_str = f"{formatear_numero(dia_data['rojo'])} - {formatear_numero(dia_data['azul'])}"
                dia_data["historial"].insert(0, {"equipo": "Azul", "accion": accion, "hora": hora,
                                                 "marcador": marcador_str})
        guardar_estado()

    # --- Selector de Días ---
    botones_dias = []

    def seleccionar_dia(e):
        dia_num = e.control.data
        if dia_num <= state["desbloqueadoHasta"]:
            state["diaActual"] = dia_num
            guardar_estado()

    for i in range(1, 6):
        btn = ft.Container(
            content=ft.Text(f"Día {i}", size=12, weight=ft.FontWeight.BOLD),
            alignment=ft.Alignment(0.0, 0.0),
            padding=ft.Padding(0, 10, 0, 10),
            border_radius=10,
            expand=True,
            data=i,
            ink=True,
            on_click=seleccionar_dia,
        )
        botones_dias.append(btn)

    # --- Botones Principales y Secundarios ---
    btn_add_rojo = ft.Container(
        content=ft.Text("+ ROJO", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#e53935",
        border_radius=16,
        padding=ft.Padding(0, 18, 0, 18),
        expand=True,
        ink=True,
        on_click=lambda _: modificar_puntos("rojo", 100)
    )
    btn_add_azul = ft.Container(
        content=ft.Text("+ AZUL", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#1e88e5",
        border_radius=16,
        padding=ft.Padding(0, 18, 0, 18),
        expand=True,
        ink=True,
        on_click=lambda _: modificar_puntos("azul", 100)
    )

    btn_sub_rojo = ft.Container(
        content=ft.Text("- 100 Rojo", size=12, weight=ft.FontWeight.W_600, color="#ff8a80"),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#16161a",
        border=ft.Border(
            top=ft.BorderSide(1, "#3c1e1e"),
            bottom=ft.BorderSide(1, "#3c1e1e"),
            left=ft.BorderSide(1, "#3c1e1e"),
            right=ft.BorderSide(1, "#3c1e1e"),
        ),
        border_radius=10,
        padding=ft.Padding(0, 8, 0, 8),
        expand=True,
        ink=True,
        on_click=lambda _: modificar_puntos("rojo", -100)
    )
    btn_sub_azul = ft.Container(
        content=ft.Text("- 100 Azul", size=12, weight=ft.FontWeight.W_600, color="#82b1ff"),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#16161a",
        border=ft.Border(
            top=ft.BorderSide(1, "#1e2a3c"),
            bottom=ft.BorderSide(1, "#1e2a3c"),
            left=ft.BorderSide(1, "#1e2a3c"),
            right=ft.BorderSide(1, "#1e2a3c"),
        ),
        border_radius=10,
        padding=ft.Padding(0, 8, 0, 8),
        expand=True,
        ink=True,
        on_click=lambda _: modificar_puntos("azul", -100)
    )

    # --- Opción Día 5: Ocultar Datos ---
    def toggle_ocultar_dia5(e):
        state["ocultarDia5"] = not state.get("ocultarDia5", False)
        guardar_estado()

    btn_ocultar_dia5 = ft.Container(
        content=ft.Text("Ocultar datos Día 5", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#2a2a35",
        border_radius=10,
        padding=ft.Padding(12, 8, 12, 8),
        ink=True,
        on_click=toggle_ocultar_dia5,
        visible=False,
    )

    # --- Finalizar Día / Torneo ---
    def finalizar_dia(e):
        if state["diaActual"] == state["desbloqueadoHasta"]:
            if state["desbloqueadoHasta"] < 5:
                state["desbloqueadoHasta"] += 1
                state["diaActual"] = state["desbloqueadoHasta"]
            elif state["desbloqueadoHasta"] == 5:
                state["torneoFinalizado"] = True
                abrir_modal_ganador()
            guardar_estado()

    btn_finalizar = ft.Container(
        content=ft.Text("Finalizar día actual ➔", size=13, weight=ft.FontWeight.BOLD, color="#888890"),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#181820",
        border=ft.Border(
            top=ft.BorderSide(1, "#282832"),
            bottom=ft.BorderSide(1, "#282832"),
            left=ft.BorderSide(1, "#282832"),
            right=ft.BorderSide(1, "#282832"),
        ),
        border_radius=12,
        padding=ft.Padding(0, 12, 0, 12),
        ink=True,
        on_click=finalizar_dia
    )

    btn_ver_ganador = ft.Container(
        content=ft.Text("🏆 Ver Resultado Final", size=14, weight=ft.FontWeight.BOLD, color="#0f0f11"),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#ffd700",
        border_radius=14,
        padding=ft.Padding(0, 14, 0, 14),
        ink=True,
        visible=False,
        on_click=lambda _: abrir_modal_ganador()
    )

    # --- Modales (Diálogos) ---
    dialog_reset = ft.AlertDialog(
        modal=True,
        bgcolor="#1e1e24",
        title=ft.Text("¿Reiniciar el torneo?", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Text("Se borrarán los 5 días y sus marcadores acumulados.", size=13, color="#aaaaaa",
                        text_align=ft.TextAlign.CENTER),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: cerrar_dialogo(dialog_reset)),
            ft.ElevatedButton("Reiniciar", bgcolor="#ff5252", color=ft.Colors.WHITE,
                              on_click=lambda _: confirmar_reset())
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def confirmar_reset():
        nonlocal state
        state = init_state()
        cerrar_dialogo(dialog_reset)
        guardar_estado()

    btn_reset_torneo = ft.Container(
        content=ft.Text("Reiniciar torneo completo", size=12, color="#888890"),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#181820",
        border_radius=10,
        padding=ft.Padding(0, 10, 0, 10),
        ink=True,
        visible=False,
        on_click=lambda _: abrir_dialogo(dialog_reset)
    )

    # --- Modal Ganador (Ampliado y con animación de fuegos artificiales) ---
    nombre_ganador = ft.Text("", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    mensaje_ganador = ft.Text("", size=14, color="#dddddd", text_align=ft.TextAlign.CENTER)

    # Generación de chispas / fuegos artificiales decorativos
    fuegos_colores = ["#ff5252", "#ffd700", "#448aff", "#2ecc71", "#ff007f", "#00ffff"]
    elementos_fuegos = []
    for _ in range(16):
        col = random.choice(fuegos_colores)
        simbolo = random.choice(["✨", "🎆", "⭐", "💥", "🎉"])
        elementos_fuegos.append(
            ft.Text(simbolo, size=random.randint(18, 28), color=col)
        )

    fuegos_row1 = ft.Row(controls=elementos_fuegos[:8], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    fuegos_row2 = ft.Row(controls=elementos_fuegos[8:], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    dialog_ganador = ft.AlertDialog(
        modal=True,
        bgcolor="#171821",
        content=ft.Container(
            width=360,
            height=380,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    fuegos_row1,
                    ft.Text("🏆", size=60),
                    nombre_ganador,
                    mensaje_ganador,
                    fuegos_row2,
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Cerrar",
                        bgcolor="#2a2a35",
                        color=ft.Colors.WHITE,
                        on_click=lambda _: cerrar_dialogo(dialog_ganador),
                        width=200
                    )
                ]
            )
        )
    )

    def abrir_dialogo(diag):
        page.dialog = diag
        diag.open = True
        page.update()

    def cerrar_dialogo(diag):
        diag.open = False
        page.update()

    def abrir_modal_ganador():
        sum_rojo = sum(state["dias"][str(i)]["rojo"] for i in range(1, 6))
        sum_azul = sum(state["dias"][str(i)]["azul"] for i in range(1, 6))

        if sum_rojo > sum_azul:
            nombre_ganador.value = "¡EQUIPO ROJO!"
            nombre_ganador.color = "#ff5252"
            mensaje_ganador.value = f"¡Felicidades al Equipo Rojo por dominar el torneo con {formatear_numero(sum_rojo)} puntos totales! 🔴"
        elif sum_azul > sum_rojo:
            nombre_ganador.value = "¡EQUIPO AZUL!"
            nombre_ganador.color = "#448aff"
            mensaje_ganador.value = f"¡Felicidades al Equipo Azul por llevarse la victoria con {formatear_numero(sum_azul)} puntos! 🔵"
        else:
            nombre_ganador.value = "¡EMPATE TÉCNICO!"
            nombre_ganador.color = "#ffd700"
            mensaje_ganador.value = f"¡Increíble duelo! Ambos equipos terminaron igualados con {formatear_numero(sum_rojo)} puntos. 🤝"

        abrir_dialogo(dialog_ganador)

    # --- Función de Renderizado Global ---
    def render():
        dia_actual = state["diaActual"]
        dia_data = state["dias"][str(dia_actual)]
        oculto = (dia_actual == 5 and state.get("ocultarDia5", False))

        # Puntos del día actual
        if oculto:
            score_rojo.value = "???"
            score_azul.value = "???"
        else:
            score_rojo.value = formatear_numero(dia_data["rojo"])
            score_azul.value = formatear_numero(dia_data["azul"])

        # Barra de botones de los 5 días
        for idx, btn_dia in enumerate(botones_dias, start=1):
            desbloqueado = idx <= state["desbloqueadoHasta"]
            activo = idx == dia_actual
            if activo:
                btn_dia.bgcolor = "#2a2a35"
                btn_dia.content.color = ft.Colors.WHITE
                btn_dia.border = ft.Border(
                    top=ft.BorderSide(1, "#555565"),
                    bottom=ft.BorderSide(1, "#555565"),
                    left=ft.BorderSide(1, "#555565"),
                    right=ft.BorderSide(1, "#555565"),
                )
            elif desbloqueado:
                btn_dia.bgcolor = "#18181c"
                btn_dia.content.color = "#aaaaaa"
                btn_dia.border = ft.Border(
                    top=ft.BorderSide(1, "#33333f"),
                    bottom=ft.BorderSide(1, "#33333f"),
                    left=ft.BorderSide(1, "#33333f"),
                    right=ft.BorderSide(1, "#33333f"),
                )
            else:
                btn_dia.bgcolor = "#141417"
                btn_dia.content.color = "#555560"
                btn_dia.border = ft.Border(
                    top=ft.BorderSide(1, "#222228"),
                    bottom=ft.BorderSide(1, "#222228"),
                    left=ft.BorderSide(1, "#222228"),
                    right=ft.BorderSide(1, "#222228"),
                )

        # Sumatoria acumulada total
        if state.get("ocultarDia5", False) and state["desbloqueadoHasta"] == 5:
            total_rojo.value = "???"
            total_azul.value = "???"
        else:
            sum_rojo = sum(state["dias"][str(i)]["rojo"] for i in range(1, 6))
            sum_azul = sum(state["dias"][str(i)]["azul"] for i in range(1, 6))
            total_rojo.value = formatear_numero(sum_rojo)
            total_azul.value = formatear_numero(sum_azul)

        # Botón de visibilidad Día 5
        if dia_actual == 5:
            btn_ocultar_dia5.visible = True
            btn_ocultar_dia5.content.value = "🔒 Revelar datos Día 5" if state.get("ocultarDia5",
                                                                                  False) else "👁️ Ocultar datos Día 5"
            btn_ocultar_dia5.bgcolor = "#e67e22" if state.get("ocultarDia5", False) else "#2a2a35"
        else:
            btn_ocultar_dia5.visible = False

        # Historial del día
        titulo_historial.value = f"REGISTRO DÍA {dia_actual}"
        total_registros.value = f"{len(dia_data['historial'])} anotaciones"
        lista_historial.controls.clear()

        if oculto:
            lista_historial.controls.append(
                ft.Container(
                    content=ft.Text("🔒 Datos ocultos para mantener el suspenso.", color="#888890", size=12),
                    padding=10,
                    alignment=ft.Alignment(0.0, 0.0)
                )
            )
        else:
            for item in dia_data["historial"]:
                tag_color = "#ff5252" if item["equipo"] == "Rojo" else "#448aff"
                item_container = ft.Container(
                    bgcolor="#1e1e24",
                    border_radius=8,
                    padding=ft.Padding(12, 6, 12, 6),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(f"{item['accion']}", size=12, color="#dddddd"),
                                    ft.Text(f"{item['equipo']}", size=12, weight=ft.FontWeight.BOLD, color=tag_color),
                                    ft.Text(f"({item['marcador']})", size=12, color="#888890"),
                                ],
                                spacing=5
                            ),
                            ft.Text(item["hora"], size=11, color="#555560")
                        ]
                    )
                )
                lista_historial.controls.append(item_container)

        # Estado de botones de finalización
        if state["torneoFinalizado"]:
            btn_finalizar.visible = False
            btn_ver_ganador.visible = True
            btn_reset_torneo.visible = True
        else:
            btn_ver_ganador.visible = False
            btn_reset_torneo.visible = False
            btn_finalizar.visible = True
            btn_finalizar.content.value = "Finalizar Torneo (Día 5) 🏁" if dia_actual == 5 else f"Finalizar día {dia_actual} ➔"

        page.update()

    # --- Construcción y montaje de la interfaz ---
    card_total = ft.Container(
        bgcolor="#14141c",
        border_radius=14,
        padding=ft.Padding(18, 12, 18, 12),
        border=ft.Border(
            top=ft.BorderSide(1, "#282832"),
            bottom=ft.BorderSide(1, "#282832"),
            left=ft.BorderSide(1, "#282832"),
            right=ft.BorderSide(1, "#282832"),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("SUMA TOTAL (5 DÍAS)", size=12, color="#888890", weight=ft.FontWeight.BOLD),
                ft.Row(controls=[total_rojo, ft.Text("-", size=18, color="#555560"), total_azul], spacing=5)
            ]
        )
    )

    card_historial = ft.Container(
        bgcolor="#16161a",
        border_radius=14,
        padding=14,
        border=ft.Border(
            top=ft.BorderSide(1, "#222228"),
            bottom=ft.BorderSide(1, "#222228"),
            left=ft.BorderSide(1, "#222228"),
            right=ft.BorderSide(1, "#222228"),
        ),
        content=ft.Column(
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[titulo_historial, total_registros]),
                lista_historial
            ],
            spacing=10
        )
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=botones_dias, spacing=6),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[score_rojo, divider_text, score_azul],
                       spacing=20),
                btn_ocultar_dia5,
                ft.Row(controls=[btn_add_rojo, btn_add_azul], spacing=12),
                ft.Row(controls=[btn_sub_rojo, btn_sub_azul], spacing=12),
                card_total,
                btn_finalizar,
                btn_ver_ganador,
                btn_reset_torneo,
                card_historial
            ],
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
    )

    render()


if __name__ == "__main__":
    ft.app(target=main)