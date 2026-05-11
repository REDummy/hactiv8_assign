import math
from datetime import datetime


def hitung_subtotal(unit, harga_satuan):
    return unit*harga_satuan


def hitung_diskon(subtotal, persen_diskon=0):
    return subtotal*persen_diskon/100


def hitung_total(subtotal, persen_diskon=0):
    return subtotal - hitung_diskon(subtotal, persen_diskon)


def buat_laporan(data_jual, pct_diskon=0):
    detail = []
    total_semua = 0
    total_unit = 0

    for item in data_jual:
        subtotal = hitung_subtotal(item["unit"], item["harga_satuan"])
        diskon = hitung_diskon(subtotal, pct_diskon)
        total = hitung_total(subtotal, pct_diskon)

    total_semua += total
    total_unit += item["unit"]

    detail.append({
        **item,
        "subtotal": subtotal,
        "diskon": diskon,
        "total": total
    })

    rata_unit = round(total_unit / len(data_jual), 2)

    return {
        "detail": detail,
        "grand_total": total_semua,
        "rata_unit": rata_unit
    }


def tambahkan_timestamp(laporan):
    bulan_indo = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]

    now = datetime.now()
    formatted = f"{now.day} {bulan_indo[now.month-1]} {now.year}, {now.strftime('%H:%M:%S')}"

    laporan["dibuat_pada"] = formatted
    return laporan


def statistik_penjualan(data_penjualan):
    subtotals = []
    total_unit = 0

    for item in data_penjualan:
        subtotal = hitung_subtotal(item["unit"], item["harga_satuan"])
        subtotals.append(subtotal)
        total_unit += item["unit"]

    mean = sum(subtotals) / len(subtotals)

    variance = sum((x - mean) ** 2 for x in subtotals) / len(subtotals)
    std_dev = math.sqrt(variance)

    return {
        "total_unit": total_unit,
        "max_subtotal": max(subtotals),
        "min_subtotal": min(subtotals),
        "std_subtotal": std_dev
    }
