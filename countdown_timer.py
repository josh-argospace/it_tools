import sys
import time
import tkinter as tk

class CountdownTimer:
    def __init__(self, master, init_d=0, init_h=0, init_m=5, init_s=0):
        self.master = master
        self.master.title("Countdown Timer")
        self.master.minsize(380, 240)

        # State
        self.running = False
        self.end_monotonic = None
        self.after_id = None
        self.flash_after_id = None
        self.flash_state = False
        self.init_values = (init_d, init_h, init_m, init_s)
        self.remaining = self._clamp_total(*self.init_values)

        # Styles
        self.bg_normal = "#101418"
        self.bg_flash_a = "#202A34"
        self.bg_flash_b = "#C0392B"
        self.fg_normal = "#E9EDF1"

        self.master.configure(bg=self.bg_normal)

        # Inputs frame (read-only labels)
        self.top = tk.Frame(master, bg=self.bg_normal)
        self.top.pack(padx=12, pady=(12, 6), fill="x")

        self.lbl_d = tk.Label(self.top, text=f"{init_d} D", font=("Consolas", 14), bg=self.bg_normal, fg=self.fg_normal)
        self.lbl_h = tk.Label(self.top, text=f"{init_h:02d} H", font=("Consolas", 14), bg=self.bg_normal, fg=self.fg_normal)
        self.lbl_m = tk.Label(self.top, text=f"{init_m:02d} M", font=("Consolas", 14), bg=self.bg_normal, fg=self.fg_normal)
        self.lbl_s = tk.Label(self.top, text=f"{init_s:02d} S", font=("Consolas", 14), bg=self.bg_normal, fg=self.fg_normal)

        self.lbl_d.pack(side="left", padx=6)
        self.lbl_h.pack(side="left", padx=6)
        self.lbl_m.pack(side="left", padx=6)
        self.lbl_s.pack(side="left", padx=6)

        # Display
        self.display = tk.Label(
            master,
            text=self._fmt(self.remaining),
            font=("Consolas", 64, "bold"),
            bg=self.bg_normal,
            fg=self.fg_normal
        )
        self.display.pack(padx=12, pady=6, fill="both", expand=True)

        # Start Button
        self.btn_start = tk.Button(master, text="Start", command=self.start, width=12,
                                   bg="#2C3E50", fg=self.fg_normal,
                                   activebackground="#34495E", activeforeground=self.fg_normal,
                                   relief="flat", padx=8, pady=6)
        self.btn_start.pack(pady=(0, 6))

        # Always on top checkbox
        self.var_topmost = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(
            master, text="Always on top", variable=self.var_topmost,
            command=self._apply_topmost, bg=self.bg_normal, fg=self.fg_normal,
            activebackground=self.bg_normal, activeforeground=self.fg_normal,
            selectcolor="#1A2129"
        )
        chk.pack(pady=(0, 12))

    def _clamp_total(self, d, h, m, s):
        total = d * 86400 + h * 3600 + m * 60 + s
        return max(0, int(total))

    def start(self):
        if not self.running:
            if self.remaining <= 0:
                return
            self.running = True
            self.end_monotonic = time.monotonic() + self.remaining + 0.05
            self._cancel_flash()
            self.top.pack_forget()   # Hide inputs
            self.btn_start.pack_forget()  # Hide start button
            self._tick()

    def _tick(self):
        if not self.running:
            return
        now = time.monotonic()
        left = int(max(0, round(self.end_monotonic - now)))
        if left != self.remaining:
            self.remaining = left
            self._update_display()
        if self.remaining <= 0:
            self.running = False
            self._cancel_after()
            self._on_finish()
            return
        self.after_id = self.master.after(100, self._tick)

    def _update_display(self):
        self.display.config(text=self._fmt(self.remaining))

    def _fmt(self, total_seconds):
        d = total_seconds // 86400
        h = (total_seconds % 86400) // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        if d > 0:
            return f"{d}d {h:02d}:{m:02d}:{s:02d}"
        elif h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        else:
            return f"{m:02d}:{s:02d}"

    def _apply_topmost(self):
        try:
            self.master.wm_attributes("-topmost", bool(self.var_topmost.get()))
        except tk.TclError:
            pass

    def _on_finish(self):
        try:
            self.master.bell()
        except Exception:
            pass
        self._start_flash()

    def _start_flash(self):
        self.flash_state = not self.flash_state
        self.master.configure(bg=self.bg_flash_a if self.flash_state else self.bg_flash_b)
        self.display.configure(bg=self.master["bg"])
        if self.flash_after_id is None:
            self.flash_deadline = time.monotonic() + 10
        if time.monotonic() < self.flash_deadline:
            self.flash_after_id = self.master.after(200, self._start_flash)
        else:
            self._cancel_flash()
            self.master.configure(bg=self.bg_normal)
            self.display.configure(bg=self.bg_normal)

    def _cancel_after(self):
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)
            self.after_id = None

    def _cancel_flash(self):
        if self.flash_after_id is not None:
            self.master.after_cancel(self.flash_after_id)
            self.flash_after_id = None

def parse_cli_default():
    if len(sys.argv) < 2:
        return 0, 0, 5, 0
    arg = sys.argv[1]
    try:
        if ":" in arg:
            parts = [int(p) for p in arg.split(":")]
            if len(parts) == 4:
                d, h, m, s = parts
            elif len(parts) == 3:
                d = 0
                h, m, s = parts
            elif len(parts) == 2:
                d = h = 0
                m, s = parts
            else:
                raise ValueError
            total = d * 86400 + h * 3600 + m * 60 + s
        else:
            total = int(arg)
        d = total // 86400
        h = (total % 86400) // 3600
        m = (total % 3600) // 60
        s = total % 60
        return d, h, m, s
    except Exception:
        return 0, 0, 5, 0

def main():
    init_d, init_h, init_m, init_s = parse_cli_default()
    root = tk.Tk()
    CountdownTimer(root, init_d, init_h, init_m, init_s)
    root.mainloop()

if __name__ == "__main__":
    main()
