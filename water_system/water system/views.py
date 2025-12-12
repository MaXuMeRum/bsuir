import tkinter as tk
from tkinter import ttk, messagebox
from .users import Dispatcher, Hydrologist, Administrator
from .processes import MonitoringProcess, PlanningProcess, ReportingProcess
from .decision import DecisionEngine

class BaseApp(tk.Tk):
    def __init__(self, reservoirs, controllers):
        super().__init__()
        self.title('ИС управления водными ресурсами')
        self.geometry('900x500')
        self.reservoirs = reservoirs
        self.controllers = controllers
        self.engine = DecisionEngine()

        lbl = ttk.Label(self, text='Выберите роль пользователя', font=('Arial', 16))
        lbl.pack(pady=10)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text='Dispatcher', width=20, command=self.open_dispatcher).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Hydrologist', width=20, command=self.open_hydrologist).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Administrator', width=20, command=self.open_admin).pack(side='left', padx=5)

    def open_dispatcher(self):
        DispatcherPanel(self, self.reservoirs, self.controllers)

    def open_hydrologist(self):
        HydrologistPanel(self, self.reservoirs)

    def open_admin(self):
        AdminPanel(self, self.reservoirs)

class DispatcherPanel(tk.Toplevel):
    def __init__(self, master, reservoirs, controllers):
        super().__init__(master)
        self.title('Dispatcher Panel')
        self.reservoirs = reservoirs
        self.controllers = controllers
        self.proc = MonitoringProcess(DecisionEngine())
        self.create_widgets()

    def create_widgets(self):
        cols = ('id','level','capacity','action')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c.title())
        self.tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text='Refresh', command=self.refresh).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Acknowledge Alert', command=self.ack_alert).pack(side='left', padx=5)
        self.refresh()

    def refresh(self):
        # sample sensors then update table
        for ctrl in self.controllers:
            ctrl.sample_all()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in self.reservoirs:
            res = self.proc.run(r)
            self.tree.insert('', 'end', values=(r.id, f"{res['level']:.3f}", f"{r.capacity}", res['decision']['action']))

    def ack_alert(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo('Info','Select reservoir row first')
            return
        row = sel[0]
        vals = self.tree.item(row,'values')
        messagebox.showinfo('Ack','Acknowledged alerts for ' + vals[0])

class HydrologistPanel(tk.Toplevel):
    def __init__(self, master, reservoirs):
        super().__init__(master)
        self.title('Hydrologist Panel')
        self.reservoirs = reservoirs
        self.proc = PlanningProcess(DecisionEngine())
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill='x', pady=5)
        ttk.Label(frame, text='Expected rainfall (mm):').pack(side='left', padx=5)
        self.rain_entry = ttk.Entry(frame); self.rain_entry.pack(side='left')
        ttk.Button(frame, text='Simulate', command=self.simulate).pack(side='left', padx=5)

        self.text = tk.Text(self, height=15)
        self.text.pack(fill='both', expand=True, padx=5, pady=5)

    def simulate(self):
        try:
            mm = float(self.rain_entry.get())
        except Exception:
            messagebox.showerror('Error','Enter valid rainfall mm')
            return
        self.text.delete('1.0', tk.END)
        for r in self.reservoirs:
            res = self.proc.simulate_rainfall(r, mm)
            self.text.insert(tk.END, f"Reservoir {r.name}:\nSimulated level: {res['simulated_level']:.3f}\nDecision: {res['decision']}\nForecast: {res['forecast']}\n\n")

class AdminPanel(tk.Toplevel):
    def __init__(self, master, reservoirs):
        super().__init__(master)
        self.title('Administrator Panel')
        self.reservoirs = reservoirs
        self.proc = ReportingProcess()
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self, text='Generate Report', command=self.generate).pack(pady=5)
        self.text = tk.Text(self, height=20)
        self.text.pack(fill='both', expand=True, padx=5, pady=5)

    def generate(self):
        history = [r.level for r in self.reservoirs]
        rpt = self.proc.generate_report(history)
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, 'Moving average:\n' + str(rpt['moving_average']) + '\n\nLong forecast:\n' + str(rpt['long_forecast']))
