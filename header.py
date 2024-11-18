import requests
from rich import print
from rich.table import Table

# Header analyzer
def analyze_security_headers(headers):
    """
    Menganalisis header keamanan dalam respons HTTP dan memberikan rekomendasi.
    """
    print("\n[bold blue]Analisis Header Keamanan:[/bold blue]\n")

    # Tabel hasil analisis
    table = Table(title="Analisis Header", show_lines=True)
    table.add_column("Header", style="bold magenta")
    table.add_column("Status", style="bold cyan")
    table.add_column("Rekomendasi", style="bold yellow")

    # Daftar header yang akan dianalisis
    important_headers = {
        "Server": "Hindari mengungkapkan detail server, gunakan header kosong atau masking.",
        "X-Powered-By": "Hindari mengungkapkan framework/teknologi yang digunakan.",
        "Set-Cookie": "Pastikan atribut Secure, HttpOnly, dan SameSite diatur dengan benar.",
        "Content-Security-Policy": "Tambahkan CSP untuk mencegah serangan XSS.",
        "Strict-Transport-Security": "Aktifkan HSTS untuk menghindari downgrade ke HTTP.",
        "Access-Control-Allow-Origin": "Periksa apakah CORS diatur dengan benar. Hindari menggunakan '*'.",
        "X-Frame-Options": "Gunakan SAMEORIGIN untuk mencegah clickjacking.",
        "Referrer-Policy": "Tetapkan no-referrer untuk menghindari kebocoran informasi.",
        "Cache-Control": "Pastikan data sensitif tidak disimpan di cache."
    }

    for header, recommendation in important_headers.items():
        if header in headers:
            if header == "Set-Cookie":
                cookies = headers[header]
                if "Secure" in cookies and "HttpOnly" in cookies:
                    status = "[bold green]Aman[/bold green]"
                else:
                    status = "[bold red]Tidak Aman[/bold red]"
                    recommendation = "Tambahkan atribut Secure dan HttpOnly pada cookie."
            else:
                status = "[bold green]Ada[/bold green]"
        else:
            status = "[bold red]Tidak Ada[/bold red]"

        # Tambahkan hasil ke tabel
        table.add_row(header, status, recommendation)

    print(table)


def analyze_http_response(url):
    """
    Menganalisis respons HTTP dan memeriksa header keamanan.
    """
    try:
        # Mengirimkan permintaan HTTP
        response = requests.get(url, allow_redirects=False)
        status_code = response.status_code
        headers = response.headers

        # Menampilkan status code
        print(f"[bold green]Menganalisis URL:[/bold green] {url}")
        print(f"[bold blue]Status Code:[/bold blue] {status_code}\n")

        # Memeriksa header keamanan
        analyze_security_headers(headers)

    except requests.exceptions.RequestException as e:
        print(f"[bold red]Error:[/bold red] Tidak dapat terhubung ke URL. Alasan: {e}")


if __name__ == "__main__":
    while True:
        # Meminta input URL dari pengguna
        url = input("Masukkan URL untuk dianalisis (atau ketik 'keluar' untuk berhenti): ").strip()
        if url.lower() == "keluar":
            print("[bold green]Keluar dari alat. Selamat tinggal![/bold green]")
            break
        analyze_http_response(url)
