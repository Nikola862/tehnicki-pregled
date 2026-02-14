import flet as ft
from supabase import create_client, Client

# --- SUPABASE PODEŠAVANJA ---
# Ovde upiši svoje podatke sa Settings -> API
URL = "https://molmdokdgtboiurxhsub.supabase.co"
KEY = "sb_publishable_3ICceFn0qVScF6wFq541GA_jR35DfGW" 

supabase: Client = create_client(URL, KEY)

def main(page: ft.Page):
    page.title = "Tehnički Pregled - Online"
    page.theme_mode = "dark"
    page.window_width = 450
    page.window_height = 800
    page.bgcolor = "#1a1c20"

    # --- ELEMENTI ---
    user_input = ft.TextField(label="Korisnik", width=300)
    pass_input = ft.TextField(label="Lozinka", password=True, width=300)
    ime_input = ft.TextField(label="Ime i Prezime", width=350)
    datum_input = ft.TextField(label="Datum (npr. 15.02.)", width=350)
    vreme_input = ft.TextField(label="Vreme (npr. 09:00)", width=350)

    def obrisi_termin(rid):
        # Brisanje iz online baze
        supabase.table("zakazivanje").delete().eq("id", rid).execute()
        prikazi_listu(None)

    def sacuvaj_termin(e):
        if ime_input.value and datum_input.value and vreme_input.value:
            # Slanje podataka na Supabase
            data = {
                "ime": ime_input.value,
                "datum": datum_input.value,
                "vreme": vreme_input.value
            }
            supabase.table("zakazivanje").insert(data).execute()
            
            ime_input.value = ""
            datum_input.value = ""
            vreme_input.value = ""
            prikazi_glavni_meni(None)
        page.update()

    def provera_logina(e):
        dozvoljeni = ["milenkovic"]
        if user_input.value.lower() in dozvoljeni and pass_input.value == "tehnicki":
            prikazi_glavni_meni(None)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Pogrešan login!"))
            page.snack_bar.open = True
            page.update()

    def prikazi_login(e=None):
        page.clean()
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.add(
            ft.Text("ONLINE SISTEM", size=25, weight="bold", color="blue"),
            user_input, pass_input,
            ft.ElevatedButton(content=ft.Text("ULOGUJ SE"), on_click=provera_logina, width=200)
        )

    def prikazi_glavni_meni(e):
        page.clean()
        page.horizontal_alignment = "center"
        page.add(
            ft.Text("NOVI TERMIN", size=22, weight="bold", color="blue"),
            ft.Container(
                padding=20,
                content=ft.Column([
                    ime_input, datum_input, vreme_input,
                    ft.ElevatedButton(
                        content=ft.Text("SAČUVAJ"),
                        on_click=sacuvaj_termin, width=350, height=50,
                        bgcolor="blue", color="white"
                    ),
                ], horizontal_alignment="center")
            ),
            ft.ElevatedButton(
                content=ft.Text("POGLEDAJ SVE TERMINE"),
                on_click=prikazi_listu, width=350, height=50
            ),
            ft.TextButton("Odjavi se", on_click=prikazi_login)
        )

    def prikazi_listu(e):
        page.clean()
        # Uzimanje podataka sa Supabase
        response = supabase.table("zakazivanje").select("*").order("datum").execute()
        rows = response.data
        
        main_list = ft.Column(scroll="auto", expand=True, spacing=15)
        danasnji_datum = ""
        
        for row in rows:
            if row["datum"] != danasnji_datum:
                danasnji_datum = row["datum"]
                main_list.controls.append(
                    ft.Container(
                        bgcolor="blue900", padding=10, border_radius=5,
                        content=ft.Text(f"DATUM: {danasnji_datum}", size=18, weight="bold")
                    )
                )
            
            main_list.controls.append(
                ft.Container(
                    bgcolor="#2a2d34", padding=15, border_radius=10,
                    content=ft.Row([
                        ft.Column([
                            ft.Text(row['ime'], size=16, weight="bold"),
                            ft.Text(f"Vreme: {row['vreme']}", color="white70"),
                        ], expand=True),
                        ft.ElevatedButton(
                            content=ft.Text("OBRIŠI"), bgcolor="red", color="white",
                            on_click=lambda e, rid=row["id"]: obrisi_termin(rid)
                        )
                    ])
                )
            )

        page.add(
            ft.Row([
                ft.TextButton("<- NAZAD", on_click=prikazi_glavni_meni),
                ft.Text("LISTA TERMINA", size=20, weight="bold")
            ]),
            main_list
        )

    prikazi_login()


ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)
