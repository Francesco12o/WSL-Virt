import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Wizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expert instalare - Wizard")
        self.geometry("700x500")
        self.resizable(False, False)

        # Stare globală
        self.install_dir = "C:/Users/NumeFals/AppFalsa"
        self.language = "Română"
        # Opțiuni avansate (Step5)
        self.adv_mod_avansat = False
        self.adv_opt_performanta = False
        self.adv_custom_path = ""
        # Opțiuni suplimentare (Step6)
        self.opt_shortcut = False
        self.opt_startup = False
        self.opt_extra_feature = False

        # Container pentru cadre
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=12, pady=12)
        self.frames = {}

        # Ordinea pașilor: 0..8 -> plasăm instalarea (Step3_Install) după confirmare (Step8), final (Step4)
        order = [
            "Step0_Terms", "Step1_Language", "Step2_Directory",
            "Step5_Advanced", "Step6_Extras", "Step7_Summary", "Step8_Confirm",
            "Step3_Install", "Step4_Finish"
        ]
        self.order = order
        for F in (Step0_Terms, Step1_Language, Step2_Directory,
                  Step5_Advanced, Step6_Extras, Step7_Summary, Step8_Confirm,
                  Step3_Install, Step4_Finish):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.current_step_index = 0
        self.show_frame(self.order[self.current_step_index])

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def next_step(self):
        if self.current_step_index < len(self.order) - 1:
            self.current_step_index += 1
            self.show_frame(self.order[self.current_step_index])

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.show_frame(self.order[self.current_step_index])

    def go_to_step(self, step_name):
        if step_name in self.order:
            self.current_step_index = self.order.index(step_name)
            self.show_frame(step_name)

    def destroy_app(self):
        self.destroy()


class Step0_Terms(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Termeni de Utilizare", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        text = tk.Text(self, height=10, wrap="word")
        text.pack(fill="both", expand=True)
        termeni = (
            "1) Aceasta este o instalare demonstrativă. Nu efectuăm modificări critice reale.\n\n"
            "2) Datele create în timpul simulării pot fi eliminate în orice moment.\n\n"
            "3) Continuând, confirmați că înțelegeți natura simulării."
        )
        text.insert("1.0", termeni)
        text.configure(state="disabled")
        self.accept_var = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(self, text="Sunt de acord cu termenii de utilizare", variable=self.accept_var, command=self.on_check)
        chk.pack(anchor="w", pady=(8,6))
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(8,0))
        cancel_btn = ttk.Button(btn_frame, text="Anulare", command=controller.destroy_app)
        cancel_btn.pack(side="right")
        self.next_btn = ttk.Button(btn_frame, text="Următorul", state=tk.DISABLED, command=controller.next_step)
        self.next_btn.pack(side="right", padx=(6,0))

    def on_check(self):
        self.next_btn.configure(state=tk.NORMAL if self.accept_var.get() else tk.DISABLED)


class Step1_Language(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Selectați limba", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        self.lang_var = tk.StringVar(value=controller.language)
        radio_frame = ttk.Frame(self)
        radio_frame.pack(anchor="w", pady=6)
        for text, val in [("Română","Română"), ("English","English"), ("Français","Français")]:
            rb = ttk.Radiobutton(radio_frame, text=text, variable=self.lang_var, value=val, command=self.on_select)
            rb.pack(anchor="w", pady=2)
        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(20,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=controller.prev_step)
        back_btn.pack(side="left")
        next_btn = ttk.Button(nav, text="Următorul", command=self.on_next)
        next_btn.pack(side="right")

    def on_select(self):
        self.controller.language = self.lang_var.get()

    def on_next(self):
        self.controller.language = self.lang_var.get()
        self.controller.next_step()


class Step2_Directory(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Selectare director instalare", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=6)
        ttk.Label(frm, text="Director implicit:").grid(row=0, column=0, sticky="w")
        self.path_var = tk.StringVar(value=controller.install_dir)
        self.entry = ttk.Entry(frm, textvariable=self.path_var, state="readonly", width=70)
        self.entry.grid(row=1, column=0, sticky="w", pady=(4,0))
        browse_btn = ttk.Button(frm, text="Răsfoire...", command=self.browse)
        browse_btn.grid(row=1, column=1, padx=(8,0))
        ttk.Label(self, text="Observație: directorul implicit este păstrat ca valoare implicită.").pack(anchor="w", pady=(8,0))
        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(20,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=controller.prev_step)
        back_btn.pack(side="left")
        next_btn = ttk.Button(nav, text="Următorul", command=self.on_next)
        next_btn.pack(side="right")

    def browse(self):
        folder = filedialog.askdirectory(title="Selectați un director (alegerea este opțională)")
        if folder:
            usar = messagebox.askyesno("Confirmare director", f"Ați selectat:\n{folder}\n\nDoriți să folosiți acest director în locul implicit?")
            if usar:
                self.controller.install_dir = folder
                self.path_var.set(folder)
            else:
                messagebox.showinfo("Director păstrat", "Directorul implicit a fost păstrat.")

    def on_next(self):
        self.controller.install_dir = self.path_var.get()
        self.controller.next_step()


class Step5_Advanced(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Setări avansate", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=6)

        # Checkbox-uri avansate
        self.mod_avansat_var = tk.BooleanVar(value=controller.adv_mod_avansat)
        cb1 = ttk.Checkbutton(frm, text="Activează modul avansat", variable=self.mod_avansat_var, command=self.on_toggle)
        cb1.pack(anchor="w", pady=2)
        self.opt_perf_var = tk.BooleanVar(value=controller.adv_opt_performanta)
        cb2 = ttk.Checkbutton(frm, text="Optimizează performanța", variable=self.opt_perf_var, command=self.on_toggle)
        cb2.pack(anchor="w", pady=2)

        # Entry-uri avansate
        ttk.Label(frm, text="Cale personalizată (opțional):").pack(anchor="w", pady=(8,0))
        self.custom_path_var = tk.StringVar(value=controller.adv_custom_path)
        self.custom_entry = ttk.Entry(frm, textvariable=self.custom_path_var, width=70)
        self.custom_entry.pack(anchor="w", pady=(4,0))

        ttk.Label(frm, text="Notă: aceste setări sunt simulate.").pack(anchor="w", pady=(8,0))

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(18,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=controller.prev_step)
        back_btn.pack(side="left")
        next_btn = ttk.Button(nav, text="Următorul", command=self.on_next)
        next_btn.pack(side="right")

    def on_toggle(self):
        # Actualizează controller imediat
        self.controller.adv_mod_avansat = self.mod_avansat_var.get()
        self.controller.adv_opt_performanta = self.opt_perf_var.get()

    def on_next(self):
        self.controller.adv_mod_avansat = self.mod_avansat_var.get()
        self.controller.adv_opt_performanta = self.opt_perf_var.get()
        self.controller.adv_custom_path = self.custom_path_var.get()
        self.controller.next_step()


class Step6_Extras(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Opțiuni suplimentare", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=6)

        self.shortcut_var = tk.BooleanVar(value=controller.opt_shortcut)
        cb1 = ttk.Checkbutton(frm, text="Creează shortcut pe desktop", variable=self.shortcut_var)
        cb1.pack(anchor="w", pady=2)
        self.startup_var = tk.BooleanVar(value=controller.opt_startup)
        cb2 = ttk.Checkbutton(frm, text="Pornește aplicația la startup", variable=self.startup_var)
        cb2.pack(anchor="w", pady=2)
        self.extra_var = tk.BooleanVar(value=controller.opt_extra_feature)
        cb3 = ttk.Checkbutton(frm, text="Activează funcție suplimentară demo", variable=self.extra_var)
        cb3.pack(anchor="w", pady=2)

        ttk.Label(frm, text="Aceste opțiuni sunt simulate și vor fi reflectate în rezumat.").pack(anchor="w", pady=(8,0))

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(18,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=controller.prev_step)
        back_btn.pack(side="left")
        next_btn = ttk.Button(nav, text="Următorul", command=self.on_next)
        next_btn.pack(side="right")

    def on_next(self):
        self.controller.opt_shortcut = self.shortcut_var.get()
        self.controller.opt_startup = self.startup_var.get()
        self.controller.opt_extra_feature = self.extra_var.get()
        self.controller.next_step()


class Step7_Summary(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Rezumat instalare", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        self.text = tk.Text(self, height=12, wrap="word")
        self.text.pack(fill="both", expand=True)
        self.text.configure(state="disabled")
        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(10,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=controller.prev_step)
        back_btn.pack(side="left")
        next_btn = ttk.Button(nav, text="Următorul", command=controller.next_step)
        next_btn.pack(side="right")

    def on_show(self):
        c = self.controller
        lines = []
        lines.append(f"Limba selectată: {c.language}")
        lines.append(f"Director instalare: {c.install_dir}")
        lines.append("")
        lines.append("Setări avansate:")
        lines.append(f"  - Modul avansat: {'Da' if c.adv_mod_avansat else 'Nu'}")
        lines.append(f"  - Optimizare performanță: {'Da' if c.adv_opt_performanta else 'Nu'}")
        lines.append(f"  - Cale personalizată: {c.adv_custom_path or '(necompletată)'}")
        lines.append("")
        lines.append("Opțiuni suplimentare:")
        lines.append(f"  - Creează shortcut: {'Da' if c.opt_shortcut else 'Nu'}")
        lines.append(f"  - Pornește la startup: {'Da' if c.opt_startup else 'Nu'}")
        lines.append(f"  - Funcție suplimentară demo: {'Da' if c.opt_extra_feature else 'Nu'}")
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", "\n".join(lines))
        self.text.configure(state="disabled")


class Step8_Confirm(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Confirmare finală", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        ttk.Label(self, text="Revizuiți setările. Apăsați 'Pornește instalarea simulată' pentru a continua.").pack(anchor="w", pady=(6,6))
        self.preview = tk.Text(self, height=8, wrap="word")
        self.preview.pack(fill="both", expand=True)
        self.preview.configure(state="disabled")

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(10,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=controller.prev_step)
        back_btn.pack(side="left")
        start_btn = ttk.Button(nav, text="Pornește instalarea simulată", command=self.start_install)
        start_btn.pack(side="right")
        cancel_btn = ttk.Button(nav, text="Anulare", command=controller.destroy_app)
        cancel_btn.pack(side="right", padx=(6,0))

    def on_show(self):
        # Actualizăm previzualizarea
        c = self.controller
        lines = [
            f"Limba: {c.language}",
            f"Director: {c.install_dir}",
            f"Mod avansat: {'Da' if c.adv_mod_avansat else 'Nu'}",
            f"Optimizare performanță: {'Da' if c.adv_opt_performanta else 'Nu'}",
            f"Cale personalizată: {c.adv_custom_path or '(necompletată)'}",
            f"Creează shortcut: {'Da' if c.opt_shortcut else 'Nu'}",
            f"Pornește la startup: {'Da' if c.opt_startup else 'Nu'}",
            f"Funcție suplimentară demo: {'Da' if c.opt_extra_feature else 'Nu'}",
        ]
        self.preview.configure(state="normal")
        self.preview.delete("1.0", tk.END)
        self.preview.insert("1.0", "\n".join(lines))
        self.preview.configure(state="disabled")

    def start_install(self):
        # Navigăm la Step3_Install care este plasat după confirmare în order
        # Resetăm progresul înainte de a porni
        install_frame = self.controller.frames["Step3_Install"]
        if hasattr(install_frame, "reset_for_install"):
            install_frame.reset_for_install()
        self.controller.go_to_step("Step3_Install")


class Step3_Install(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Instalare în desfășurare", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", pady=6)
        self.status_label = ttk.Label(status_frame, text="Stare: Pregătire...")
        self.status_label.pack(anchor="w", pady=(0,6))
        self.progress = ttk.Progressbar(status_frame, orient="horizontal", length=600, mode="determinate")
        self.progress.pack(anchor="w", pady=(0,6))
        self.progress["maximum"] = 100
        self.progress["value"] = 0

        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", pady=(10,0))
        ttk.Label(control_frame, text="Control instalare:").pack(anchor="w")
        self.advance_btn = ttk.Button(control_frame, text="Simulează următorul pas", command=self.advance_step)
        self.advance_btn.pack(anchor="w", pady=(6,4))

        auto_frame = ttk.Frame(self)
        auto_frame.pack(fill="x", pady=(6,0))
        self.auto_var = tk.BooleanVar(value=False)
        self.auto_chk = ttk.Checkbutton(auto_frame, text="Avans automat (folosește controller.after)", variable=self.auto_var, command=self.toggle_auto)
        self.auto_chk.pack(anchor="w")

        self.steps = [
            (10, "Initializare..."),
            (40, "Copiere fișiere..."),
            (70, "Instalare componente..."),
            (90, "Configurare registri și permisiuni..."),
            (100, "Curățare finală...")
        ]
        self.current_step = 0

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(20,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=self.on_back)
        back_btn.pack(side="left")
        cancel_btn = ttk.Button(nav, text="Anulare", command=controller.destroy_app)
        cancel_btn.pack(side="right")

    def on_show(self):
        # Nu reseta automat la revenire, dar putem afișa starea curentă
        pass

    def reset_for_install(self):
        self.progress["value"] = 0
        self.current_step = 0
        self.status_label.config(text="Stare: Pregătire...")
        self.auto_var.set(False)
        self.advance_btn.configure(state=tk.NORMAL)

    def advance_step(self):
        if self.current_step < len(self.steps):
            value, text = self.steps[self.current_step]
            self.progress["value"] = value
            self.status_label.config(text=f"Stare: {text} ({value}%)")
            self.current_step += 1
            if self.progress["value"] >= 100:
                self.after(700, lambda: self.controller.next_step())

    def toggle_auto(self):
        if self.auto_var.get():
            self.advance_btn.configure(state=tk.DISABLED)
            self._auto_advance()
        else:
            self.advance_btn.configure(state=tk.NORMAL)

    def _auto_advance(self):
        if not self.auto_var.get():
            return
        if self.current_step < len(self.steps):
            value, text = self.steps[self.current_step]
            self.progress["value"] = value
            self.status_label.config(text=f"Stare: {text} ({value}%)")
            self.current_step += 1
            self.after(600, self._auto_advance)
        else:
            self.after(700, lambda: self.controller.next_step())

    def on_back(self):
        if self.progress["value"] > 0:
            ok = messagebox.askyesno("Confirmare", "Progresul de instalare va fi resetat. Continuați?")
            if not ok:
                return
        # revenim la confirmare (Step8)
        self.controller.go_to_step("Step8_Confirm")


class Step4_Finish(ttk.Frame):
    def __init__(self, parent, controller: Wizard):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Finalizare", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,6))
        self.msg_label = ttk.Label(self, text="Instalarea a fost finalizată!", font=("Segoe UI", 12))
        self.msg_label.pack(anchor="w", pady=(6,6))
        loc_frame = ttk.Frame(self)
        loc_frame.pack(fill="x", pady=(6,0))
        ttk.Label(loc_frame, text="Locație instalare:").grid(row=0, column=0, sticky="w")
        self.final_path_var = tk.StringVar(value=controller.install_dir)
        self.final_entry = ttk.Entry(loc_frame, textvariable=self.final_path_var, width=70)
        self.final_entry.grid(row=1, column=0, sticky="w", pady=(4,0))
        browse_btn = ttk.Button(loc_frame, text="Răsfoire...", command=self.browse_and_set)
        browse_btn.grid(row=1, column=1, padx=(8,0))
        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(20,0))
        back_btn = ttk.Button(nav, text="Înapoi", command=self.on_back)
        back_btn.pack(side="left")
        finish_btn = ttk.Button(nav, text="Finalizare", command=controller.destroy_app)
        finish_btn.pack(side="right")

    def on_show(self):
        self.final_path_var.set(self.controller.install_dir)

    def browse_and_set(self):
        folder = filedialog.askdirectory(title="Selectați directorul final de instalare")
        if folder:
            self.controller.install_dir = folder
            self.final_path_var.set(folder)
            messagebox.showinfo("Director setat", f"Locația finală setată la:\n{folder}")

    def on_back(self):
        # Revenim la Step3_Install (care a dus la finish)
        self.controller.go_to_step("Step3_Install")


if __name__ == "__main__":
    app = Wizard()
    app.mainloop()
