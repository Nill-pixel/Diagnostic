import flet as ft


class MyPieChart(ft.UserControl):
    def __init__(self, initial_predictions):
        super().__init__()
        self.predictions = initial_predictions  # Armazena as previsões iniciais

        # Definir estilos e propriedades normais
        self.normal_radius = 100
        self.hover_radius = 110
        self.normal_title_style = ft.TextStyle(
            size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
        )
        self.hover_title_style = ft.TextStyle(
            size=16,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        )
        self.normal_badge_size = 40
        self.hover_badge_size = 50

        # Inicializar o gráfico com base nas previsões iniciais
        self.build()

    def badge(self, icon, size):
        return ft.Container(
            ft.Icon(icon),
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.BROWN),
            border_radius=size / 2,
            bgcolor=ft.colors.WHITE,
        )

    def on_chart_event(self, e: ft.PieChartEvent):
        for idx, section in enumerate(self.chart.sections):
            if idx == e.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
        self.chart.update()

    def build(self):
        sections = []
        colors = [ft.colors.BLUE, ft.colors.YELLOW, ft.colors.PURPLE, ft.colors.GREEN]
        icons = [
            ft.icons.AC_UNIT,
            ft.icons.ACCESS_ALARM,
            ft.icons.APPLE,
            ft.icons.PEDAL_BIKE,
        ]

        for idx, (label, probability) in enumerate(self.predictions.items()):
            sections.append(
                ft.PieChartSection(
                    probability * 100,
                    title=f"{probability * 100:.2f}%",
                    title_style=self.normal_title_style,
                    color=colors[idx],
                    radius=self.normal_radius,
                    badge=self.badge(icons[idx], self.normal_badge_size),
                    badge_position=0.98,
                )
            )

        self.chart = ft.PieChart(
            sections=sections,
            sections_space=0,
            center_space_radius=0,
            on_chart_event=self.on_chart_event,
            expand=True,
        )
        return self.chart

    def update_predictions(self, new_predictions):
        self.predictions = new_predictions
        sections = self.chart.sections

        for idx, (label, probability) in enumerate(self.predictions.items()):
            sections[idx].percentage = probability * 100
            sections[idx].title = f"{probability * 100:.2f}%"

        self.chart.update()
