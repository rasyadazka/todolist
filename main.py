#!/usr/bin/env python3
"""
Aplikasi To-Do sederhana (CLI) dalam bahasa Indonesia.
Fitur:
- Menambahkan tugas dengan nama dan waktu tenggat (deadline)
- Menampilkan tugas yang diurutkan berdasarkan tenggat waktu (terdekat dulu)
- Menghapus tugas
- Menyimpan dan memuat tugas dari file `tasks.json`

Format tanggal yang diterima: `YYYY-MM-DD` atau `YYYY-MM-DD HH:MM`
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import os
from typing import List

TASKS_FILE = "tasks.json"

@dataclass
class Task:
    name: str
    due: datetime

    def to_dict(self):
        return {"name": self.name, "due": self.due.isoformat()}

    @staticmethod
    def from_dict(d):
        return Task(name=d["name"], due=datetime.fromisoformat(d["due"]))


def load_tasks() -> List[Task]:
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(item) for item in data]


def save_tasks(tasks: List[Task]):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)


def parse_datetime(input_str: str) -> datetime | None:
    input_str = input_str.strip()
    formats = ["%Y-%m-%d %H:%M", "%Y-%m-%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(input_str, fmt)
            # If no time provided, set to end of day
            if fmt == "%Y-%m-%d":
                dt = dt.replace(hour=23, minute=59)
            return dt
        except ValueError:
            continue
    return None


def add_task(tasks: List[Task]):
    name = input("Nama tugas: ").strip()
    if not name:
        print("Nama tugas tidak boleh kosong.")
        return
    due_str = input("Tenggat waktu (contoh: 2026-02-05 14:30 atau 2026-02-05): ").strip()
    due = parse_datetime(due_str)
    if due is None:
        print("Format tanggal tidak dikenali. Gunakan YYYY-MM-DD atau YYYY-MM-DD HH:MM")
        return
    tasks.append(Task(name=name, due=due))
    save_tasks(tasks)
    print(f"Tugas '{name}' ditambahkan dengan tenggat {due}.")


def list_tasks(tasks: List[Task]):
    if not tasks:
        print("Tidak ada tugas.")
        return
    tasks_sorted = sorted(tasks, key=lambda t: t.due)
    print("\nDaftar tugas (diurutkan berdasarkan tenggat waktu):")
    print("-------------------------------------------------")
    now = datetime.now()
    for i, t in enumerate(tasks_sorted, start=1):
        status = "(telat)" if t.due < now else ""
        print(f"{i}. {t.name} — tenggat: {t.due.strftime('%Y-%m-%d %H:%M')} {status}")
    print("-------------------------------------------------\n")


def remove_task(tasks: List[Task]):
    if not tasks:
        print("Tidak ada tugas untuk dihapus.")
        return
    list_tasks(tasks)
    try:
        idx = int(input("Masukkan nomor tugas yang ingin dihapus: "))
    except ValueError:
        print("Masukkan nomor yang valid.")
        return
    tasks_sorted = sorted(tasks, key=lambda t: t.due)
    if idx < 1 or idx > len(tasks_sorted):
        print("Nomor tugas tidak valid.")
        return
    task = tasks_sorted[idx - 1]
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Tugas '{task.name}' dihapus.")


def clear_tasks(tasks: List[Task]):
    confirm = input("Yakin ingin menghapus semua tugas? (y/N): ")
    if confirm.lower() == "y":
        tasks.clear()
        save_tasks(tasks)
        print("Semua tugas dihapus.")
    else:
        print("Dibatalkan.")


def show_menu():
    print("Aplikasi To-Do (urut berdasarkan tenggat waktu)")
    print("1. Tambah tugas")
    print("2. Lihat daftar tugas")
    print("3. Hapus tugas")
    print("4. Hapus semua tugas")
    print("5. Keluar")


def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Pilih nomor: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            clear_tasks(tasks)
        elif choice == "5":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak dikenali. Masukkan nomor antara 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDibatalkan oleh pengguna.")
