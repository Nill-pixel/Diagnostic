from components import PieChart  # Supondo que PieChart seja sua classe para gráficos
import flet as ft
import aiohttp
import json


async def send_data(
    data, image_file_path=None, api_url="http://localhost:5000/predict"
):
    headers = {"Content-Type": "application/json"}

    if image_file_path:
        form_data = aiohttp.FormData()
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
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                api_url, data=json.dumps(data), headers=headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    return {"error": "Erro ao enviar dados para a API"}


class Symptom(ft.Column):
    def __init__(self, symptom_name, api_name):
        super().__init__()
        self.symptom_name = symptom_name
        self.api_name = api_name  # Nome do sintoma conforme esperado pela API
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
            self.selected_file_path = None
            self.image_path_text.value = "Nenhuma imagem selecionada"
        self.update()

    def open_file_picker(self, e):
        self.image_upload_button.pick_files(
            allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]
        )


class MedicineApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.new_symptom = ft.Text("Diagnóstico Médico", size=30)
        self.symptoms_grid = ft.GridView(
            runs_count=3,
            max_extent=200,
            child_aspect_ratio=4.0,
            spacing=2,
            run_spacing=2,
        )
        self.image_upload = DiagnosticImage()
        self.result_text = ft.Text()
        self.pie_chart = None

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="sintomas"), ft.Tab(text="imagem")],
        )

        self.age_input = ft.TextField(label="Idade")
        self.sex_input = ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("female", "Feminino"),
                ft.dropdown.Option("male", "Masculino"),
                ft.dropdown.Option("not to say", "Não informado"),
            ],
        )
        self.nature_input = ft.Dropdown(
            label="Natureza",
            options=[
                ft.dropdown.Option("", "Não especificado"),
                ft.dropdown.Option("high", "Alto"),
                ft.dropdown.Option("low", "Baixo"),
                ft.dropdown.Option("medium", "Médio"),
            ],
        )
        self.treatment_input = ft.Dropdown(
            label="Tratamento",
            options=[
                ft.dropdown.Option(
                    "Adaptive servo-ventilation", "Ventilação servo-adaptativa"
                ),
                ft.dropdown.Option("Antibiotic", "Antibiótico"),
                ft.dropdown.Option("Chemotherapy", "Quimioterapia"),
                ft.dropdown.Option("Cough medicine", "Remédio para tosse"),
                ft.dropdown.Option("Diuretics", "Diuréticos"),
                ft.dropdown.Option(
                    "Intrapulmonary Percussive Ventilation",
                    "Ventilação por percussão intrapulmonar",
                ),
                ft.dropdown.Option("Intravenous fluids", "Fluidos intravenosos"),
                ft.dropdown.Option("Mepolizumab", "Mepolizumabe"),
                ft.dropdown.Option("Omalizumab", "Omalizumabe"),
                ft.dropdown.Option("Oseltamivir", "Oseltamivir"),
                ft.dropdown.Option("Pulmonary rehabilitation", "Reabilitação pulmonar"),
                ft.dropdown.Option("Surgery", "Cirurgia"),
                ft.dropdown.Option("aspirin", "Aspirina"),
                ft.dropdown.Option("consult a doctor", "Consulte um médico"),
                ft.dropdown.Option("consult doctor", "Consulte um médico"),
                ft.dropdown.Option("ethambutol", "Etambutol"),
                ft.dropdown.Option(
                    "isotonic sodium chloride solution", "Solução salina isotônica"
                ),
                ft.dropdown.Option("itraconazole", "Itraconazol"),
                ft.dropdown.Option("oxygen", "Oxigênio"),
                ft.dropdown.Option("oxyzen", "Oxigênio"),
                ft.dropdown.Option("pyrazinamide", "Pirazinamida"),
                ft.dropdown.Option("rifampin", "Rifampicina"),
                ft.dropdown.Option("saline nose drops", "Gotas nasais salinas"),
                ft.dropdown.Option("stay away from cold places", "Evite lugares frios"),
                ft.dropdown.Option(
                    "steroids to reduce inflammation",
                    "Esteroides para reduzir a inflamação",
                ),
                ft.dropdown.Option("surgery", "Cirurgia"),
                ft.dropdown.Option("x-ray", "Raio-X"),
            ],
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
                    self.symptoms_grid,
                    self.age_input,
                    self.sex_input,
                    self.nature_input,
                    self.treatment_input,
                    self.image_upload,
                    self.select_image_button,
                    self.submit_button,
                    self.result_text,
                ],
            ),
        ]

        # Lista de sintomas em português que serão exibidos na interface
        symptoms_list_pt = [
            "Tosse",
            "Falta de ar",
            "Febre",
            "Dor de garganta",
            "Congestão nasal",
            "Fadiga",
            "Alergia",
            "Pele azulada",
            "Congestão no peito",
            "Dor no peito",
            "Calafrios",
            "Tosse",
            # Adicione outros sintomas conforme necessário
        ]

        # Mapeamento de sintomas para API (nomes em inglês esperados pela API)
        symptoms_mapping = {
            "Tosse": "Cough",
            "Falta de ar": "Shortness of breath",
            "Febre": "Fever",
            "Dor de garganta": "Sore throat",
            "Congestão nasal": "Nasal congestion",
            "Fadiga": "Fatigue",
            "Alergia": "Allergy",
            "Pele azulada": "Bluish skin",
            "Congestão no peito": "Chest congestion",
            "Dor no peito": "Chest pain",
            "Calafrios": "Chills",
            # Adicione outros sintomas conforme necessário
        }

        for symptom_name_pt in symptoms_list_pt:
            symptom_api_name = symptoms_mapping.get(
                symptom_name_pt, symptom_name_pt.lower()
            )
            symptom = Symptom(symptom_name_pt, symptom_api_name)
            self.symptoms_grid.controls.append(symptom)

    async def on_submit(self, e):
        age = self.age_input.value
        sex = self.sex_input.value
        nature = self.nature_input.value
        treatment = self.treatment_input.value
        status = self.filter.tabs[self.filter.selected_index].text

        if status == "sintomas":
            selected_symptoms = [
                symptom.api_name
                for symptom in self.symptoms_grid.controls
                if symptom.display_symptom.value
            ]
            if selected_symptoms and age and sex and nature and treatment:
                data = {
                    "symptoms": selected_symptoms,
                    "age": age,
                    "sex": sex,
                    "nature": nature,
                    "treatment": treatment,
                }
                result = await send_data(
                    data, api_url="http://localhost:5000/predict_symptoms"
                )
                await self.show_result_dialog(result)
            else:
                self.result_text.value = "Por favor, preencha todos os campos."

        elif status == "imagem":
            if self.image_upload.selected_file_path:
                result = await send_data(
                    {},
                    self.image_upload.selected_file_path,
                    api_url="http://localhost:5000/predict_image",
                )
                await self.show_result_dialog(result)

                if "predictions" in result:
                    predictions = result["predictions"]
                    new_predictions = {
                        key: float(value.replace("%", ""))
                        for key, value in predictions.items()
                    }

                    if self.pie_chart is None:
                        self.pie_chart = PieChart.MyPieChart(new_predictions)
                        self.page.add(self.pie_chart)
                    else:
                        self.page.remove(self.pie_chart)
                        self.pie_chart = PieChart.MyPieChart(new_predictions)
                        self.page.add(self.pie_chart)

                    self.update()

            else:
                self.result_text.value = "Por favor, selecione uma imagem."

        self.update()

    async def show_result_dialog(self, result):
        if "error" in result:
            alert = ft.AlertDialog(
                title=ft.Text("Erro"), content=ft.Text(result["error"])
            )
        else:
            if "predicted_treatment" in result:
                predicted_treatment = result["predicted_treatment"]
                alert_content = ft.Column(
                    controls=[
                        ft.Text(f"Doenças Prevista: {predicted_treatment}"),
                    ]
                )
                alert = ft.AlertDialog(
                    title=ft.Text("Resultado"), content=alert_content
                )
            elif "predictions" in result:
                predictions = result["predictions"]
                new_predictions = {
                    key: float(value.replace("%", ""))
                    for key, value in predictions.items()
                }

                if self.pie_chart is None:
                    self.pie_chart = PieChart.MyPieChart(new_predictions)
                else:
                    self.pie_chart = PieChart.MyPieChart(new_predictions)

                alert_content = ft.Column(
                    controls=[ft.Text("Resultado"), self.pie_chart]
                )
                alert = ft.AlertDialog(
                    title=ft.Text("Resultado"), content=alert_content
                )

        await self.page.open(alert)

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text

        for symptom in self.symptoms_grid.controls:
            symptom.visible = status == "sintomas"
        self.age_input.visible = status == "sintomas"
        self.sex_input.visible = status == "sintomas"
        self.nature_input.visible = status == "sintomas"
        self.treatment_input.visible = status == "sintomas"
        self.image_upload.visible = status == "imagem"
        self.select_image_button.visible = status == "imagem"
        self.submit_button.visible = True

    def tabs_changed(self, e):
        self.before_update()
        self.update()


def main(page: ft.Page):
    page.title = "Diagnóstico Médico"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    app = MedicineApp()
    page.add(app)


ft.app(target=main)
