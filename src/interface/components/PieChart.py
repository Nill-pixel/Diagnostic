import flet as ft


def badge(icon, size):
    return ft.Container(
        ft.Icon(icon),
        width=size,
        height=size,
        border=ft.border.all(1, ft.colors.BROWN),
        border_radius=size / 2,
        bgcolor=ft.colors.WHITE,
    )


class MyPieChart(ft.UserControl):
    def __init__(self, initial_predictions):
        super().__init__()
        self.predictions = initial_predictions

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

        self.build()

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
        self.sections = []
        colors = [ft.colors.GREEN, ft.colors.YELLOW, ft.colors.RED]
        icons = [
            ft.icons.AC_UNIT,
            ft.icons.ACCESS_ALARM,
            ft.icons.APPLE,
        ]

        self.categories = ["Normal", "COVID", "Pneumonia"]
        for idx, category in enumerate(self.categories):
            probability = self.predictions.get(
                category, 0.0
            )  # Assume que a API já retorna float
            self.sections.append(
                ft.PieChartSection(
                    probability * 1,
                    title=f"{category} : {probability * 1:.2f}%",
                    title_style=self.normal_title_style,
                    color=colors[idx],
                    radius=self.normal_radius,
                    badge=badge(icons[idx], self.normal_badge_size),
                    badge_position=0.98,
                )
            )

        self.chart = ft.PieChart(
            sections=self.sections,
            sections_space=0,
            center_space_radius=0,
            on_chart_event=self.on_chart_event,
            expand=True,
        )
        return self.chart

    def update_predictions(self, new_predictions):
        self.predictions = new_predictions

        for idx, category in enumerate(self.categories):
            probability = self.predictions.get(
                category, 0.0
            )  # Assume que a API já retorna float
            self.sections[idx].percentage = probability * 1
            self.sections[idx].title = f"{probability * 1:.2f}%"

            # Atualiza a cor com base na categoria
            if category == "Normal":
                self.sections[idx].color = ft.colors.GREEN
            elif category == "COVID":
                self.sections[idx].color = ft.colors.YELLOW
            elif category == "Pneumonia":
                self.sections[idx].color = ft.colors.RED

        self.chart.update()
