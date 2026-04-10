import flet as ft

def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Monitor de Servicios Médicos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK # Modo oscuro

    # Ejemplo de una fila (Row) con texto y un botón
    # Importante: 'controls' debe ser una lista []
    page.add(
        ft.Row(
            controls=[
                ft.Icon(ft.icons.MEDICAL_SERVICES, color="blue", size=30),
                ft.Text("Estado del Sistema: Activo", size=20, weight="bold"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton("Ver Inventario", icon=ft.icons.LIST_ALT),
                ft.ElevatedButton("Reportar Falla", icon=ft.icons.WARNING, color="orange"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)

main()