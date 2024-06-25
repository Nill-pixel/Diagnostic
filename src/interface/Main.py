import flet as ft
from components import PieChart
import aiohttp
import asyncio


async def send_data(symptoms, image_file_path):
    api_url = "http://localhost:5000/predict"  # Substitua pelo URL da sua API
    data = {"symptoms": symptoms}

    form_data = aiohttp.FormData()
    form_data.add_field("symptoms", str(symptoms))  # Add symptoms as a string
    if image_file_path:
        form_data.add_field(
            "image", open(image_file_path, "rb"), filename=image_file_path
        )

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data=form_data) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                return {"error": "Erro ao enviar dados para a API"}


class Symptom(ft.Column):
    def __init__(self, symptom_name):
        super().__init__()
        self.symptom_name = symptom_name
        self.display_symptom = ft.Checkbox(value=False, label=self.symptom_name)
        self.controls = [self.display_symptom]


class DiagnosticImage(ft.Column):
    def __init__(self):
        super().__init__()
        self.image_path_text = ft.Text(value="Nenhuma imagem selecionada")
        self.image_upload_button = ft.FilePicker(on_result=self.on_file_picked)
        self.controls = [self.image_path_text, self.image_upload_button]
        self.selected_file_path = None

    def on_file_picked(self, e):
        if e.files:
            self.selected_file_path = e.files[0].path
            self.image_path_text.value = self.selected_file_path
        else:
            self.image_path_text.value = "Nenhuma imagem selecionada"
        self.update()

    def open_file_picker(self, e):
        self.image_upload_button.pick_files(
            allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]
        )


class MedicineApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.new_symptom = ft.Text("Medical Diagnosis By X-ray And Symptoms", size=30)
        self.symptoms = ft.Column()
        self.image_upload = DiagnosticImage()
        self.result_text = ft.Text()
        self.pie_chart = None  # Inicializa pie_chart como None

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="symptoms"), ft.Tab(text="image")],
        )

        self.width = 600
        self.select_image_button = ft.ElevatedButton(
            text="Selecionar Imagem",
            icon=ft.icons.IMAGE,
            style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREEN),
            on_click=self.image_upload.open_file_picker,
            visible=True,
        )

        self.submit_button = ft.ElevatedButton(
            text="Enviar",
            icon=ft.icons.SEND,
            style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREEN),
            on_click=self.on_submit,
            visible=True,
        )

        self.controls = [
            ft.Row(controls=[self.new_symptom]),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.symptoms,
                    self.image_upload,
                    self.select_image_button,
                    self.submit_button,
                    self.result_text,
                ],
            ),
        ]

        symptoms_list = [
            "Tosse",
            "Falta de ar",
            "Febre",
            "Dor de garganta",
            "Congestão nasal",
            "Fadiga",
        ]

        for symptom_name in symptoms_list:
            symptom = Symptom(symptom_name)
            self.symptoms.controls.append(symptom)

    def add_clicked(self, e):
        symptom = Symptom(self.new_symptom.value)
        self.symptoms.controls.append(symptom)
        self.new_symptom.value = ""
        self.update()

    async def on_submit(self, e):
        selected_symptoms = [
            cb.display_symptom.label
            for cb in self.symptoms.controls
            if cb.display_symptom.value
        ]
        status = self.filter.tabs[self.filter.selected_index].text

        if status == "symptoms":
            if selected_symptoms:
                result = await send_data(selected_symptoms, None)
                self.result_text.value = str(result)
            else:
                self.result_text.value = "Por favor, selecione os sintomas."
        elif status == "image":
            if self.image_upload.selected_file_path:
                result = await send_data([], self.image_upload.selected_file_path)
                self.result_text.value = str(result)

                # Atualizar o MyPieChart com as novas previsões
                if "predictions" in result:
                    predictions = result[
                        "predictions"
                    ]  # Recebeu as previsões diretamente
                    new_predictions = {
                        key: float(value.replace("%", ""))
                        for key, value in predictions.items()
                    }
                    if self.pie_chart is not None:
                        self.page.remove(
                            self.pie_chart
                        )  # Remover o gráfico antigo se existir
                    self.pie_chart = PieChart.MyPieChart(
                        new_predictions
                    )  # Criar um novo MyPieChart
                    self.page.add(self.pie_chart)  # Adicionar o gráfico atualizado
            else:
                self.result_text.value = "Por favor, selecione uma imagem."

        self.update()

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for symptom in self.symptoms.controls:
            symptom.visible = status == "symptoms"
        self.image_upload.visible = status == "image"
        self.select_image_button.visible = status == "image"
        self.submit_button.visible = True

    def tabs_changed(self, e):
        self.before_update()
        self.update()


def main(page: ft.Page):
    page.title = "Medical Diagnostic"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    app = MedicineApp()
    page.add(app)


ft.app(target=main)
