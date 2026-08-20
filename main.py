import flet as ft


def main(page: ft.Page):
    page.title = "Marcador de Registro Diario"
    page.bgcolor = "#111317"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 420
    page.window.height = 680
    page.window.resizable = False

    # Estructura de datos por días
    dias_registrados = [
        {"dia": "Día 1", "equipo_a": 3, "equipo_b": 1, "notas": "Primer encuentro"},
        {"dia": "Día 2", "equipo_a": 2, "equipo_b": 2, "notas": "Empate reñido"},
        {"dia": "Día 3", "equipo_a": 4, "equipo_b": 0, "notas": "Último registro activo"}
    ]

    # Estado de visibilidad para el último día
    datos_ultimo_dia_visibles = True

    # Contenedor visual dinámico
    lista_vistas = ft.Column(spacing=12, scroll=ft.ScrollMode.ADAPTIVE, expand=True)

    def alternar_visibilidad_ultimo_dia(e):
        nonlocal datos_ultimo_dia_visibles
        datos_ultimo_dia_visibles = not datos_ultimo_dia_visibles
        renderizar_marcador()

    def renderizar_marcador():
        lista_vistas.controls.clear()

        for idx, item in enumerate(dias_registrados):
            es_ultimo = (idx == len(dias_registrados) - 1)

            # Si es el último día y está oculto, enmascarar los datos
            if es_ultimo and not datos_ultimo_dia_visibles:
                score_a = "--"
                score_b = "--"
                nota = "🔒 Datos ocultos por privacidad"
                color_tarjeta = "#1f242d"
            else:
                score_a = str(item["equipo_a"])
                score_b = str(item["equipo_b"])
                nota = item["notas"]
                color_tarjeta = "#1a1d24"

            # Tarjeta de cada día
            tarjeta = ft.Container(
                bgcolor=color_tarjeta,
                border_radius=12,
                padding=15,
                border=ft.border.all(1, "#2ecc71" if es_ultimo else "#2c3e50"),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    f"{item['dia']} {'(Último Día)' if es_ultimo else ''}",
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                    color="#2ecc71" if es_ultimo else ft.Colors.WHITE,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(score_a, size=18, weight=ft.FontWeight.BOLD),
                                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                            bgcolor="#3498db",
                                            border_radius=8
                                        ),
                                        ft.Text(" - ", size=18, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text(score_b, size=18, weight=ft.FontWeight.BOLD),
                                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                            bgcolor="#e74c3c",
                                            border_radius=8
                                        ),
                                    ]
                                )
                            ]
                        ),
                        ft.Text(nota, size=13, color=ft.Colors.WHITE60),

                        # Opción exclusiva en el último día para ocultar/mostrar datos
                        ft.Container(
                            visible=es_ultimo,
                            margin=ft.margin.only(top=10),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            "Mostrar datos" if not datos_ultimo_dia_visibles else "Ocultar datos",
                                            size=13,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE
                                        ),
                                        bgcolor="#e67e22" if not datos_ultimo_dia_visibles else "#7f8c8d",
                                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                        border_radius=8,
                                        ink=True,
                                        on_click=alternar_visibilidad_ultimo_dia
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
            lista_vistas.controls.append(tarjeta)

        page.update()

    # Campos para registrar un nuevo día
    input_nombre_dia = ft.TextField(label="Nombre del Día (ej. Día 4)", bgcolor="#161920", border_radius=10)
    input_score_a = ft.TextField(label="Puntos Equipo A", keyboard_type=ft.KeyboardType.NUMBER, bgcolor="#161920",
                                 border_radius=10, expand=True)
    input_score_b = ft.TextField(label="Puntos Equipo B", keyboard_type=ft.KeyboardType.NUMBER, bgcolor="#161920",
                                 border_radius=10, expand=True)
    input_notas = ft.TextField(label="Notas / Resumen", bgcolor="#161920", border_radius=10)

    def agregar_registro(e):
        if not input_nombre_dia.value or not input_score_a.value or not input_score_b.value:
            return

        try:
            dias_registrados.append({
                "dia": input_nombre_dia.value.strip(),
                "equipo_a": int(input_score_a.value),
                "equipo_b": int(input_score_b.value),
                "notas": input_notas.value.strip() or "Sin notas adicionales"
            })
            # Limpiar campos
            input_nombre_dia.value = ""
            input_score_a.value = ""
            input_score_b.value = ""
            input_notas.value = ""
            renderizar_marcador()
        except ValueError:
            pass

    btn_agregar = ft.Container(
        content=ft.Text("Registrar Nuevo Día", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.Alignment(0.0, 0.0),
        bgcolor="#2ecc71",
        border_radius=10,
        height=45,
        ink=True,
        on_click=agregar_registro,
    )

    formulario_registro = ft.ExpansionTile(
        title=ft.Text("Añadir nuevo registro", size=14, weight=ft.FontWeight.W_500),
        controls=[
            ft.Column(
                controls=[
                    input_nombre_dia,
                    ft.Row(controls=[input_score_a, input_score_b], spacing=10),
                    input_notas,
                    btn_agregar
                ],
                spacing=10
            )
        ]
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text("Marcador de Jornadas", size=22, weight=ft.FontWeight.BOLD),
                formulario_registro,
                ft.Divider(color=ft.Colors.WHITE24),
                lista_vistas
            ],
            expand=True,
            spacing=10
        )
    )

    renderizar_marcador()


if __name__ == "__main__":
    ft.app(target=main)