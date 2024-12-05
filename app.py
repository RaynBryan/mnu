from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

# Data menu coffee shop
menu = {
    "coffee": {
        "Espresso": 20000,
        "Americano": 25000,
        "Cappuccino": 30000,
        "Latte": 35000
    },
    "tea": {
        "Green Tea": 20000,
        "Black Tea": 18000,
        "Milk Tea": 25000
    },
    "snack": {
        "Brownie": 20000,
        "Croissant": 25000,
        "Muffin": 15000
    }
}

# Variabel global untuk menyimpan pesanan pengguna
order = {}

# Halaman utama untuk menampilkan menu
@app.route('/')
def index():
    return render_template('index.html', menu=menu, order=order)

# Endpoint untuk menambahkan pesanan
@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    category = request.form.get('category')  # Kategori item
    item = request.form.get('item')  # Nama item
    quantity = int(request.form.get(f'quantity_{item}', 1))  # Ambil jumlah berdasarkan item yang dipilih

    if item in menu[category]:  # Validasi apakah item ada di menu
        order[item] = order.get(item, 0) + quantity
    return redirect(url_for('index'))

# Endpoint untuk checkout dan menampilkan struk
@app.route('/checkout')
def checkout():
    # Menghitung total harga dengan lebih efisien di Python
    start_time = time.time()  # Mulai waktu
    total_price = sum(menu[cat][item] * qty for item, qty in order.items() for cat in menu if item in menu[cat])
    end_time = time.time()  # Waktu selesai
    
    # Logging untuk melihat waktu yang dihabiskan
    print(f"Checkout time: {end_time - start_time} seconds")
    
    return render_template('checkout.html', order=order, total_price=total_price)

# Endpoint untuk menghapus pesanan
@app.route('/remove_item/<item>')
def remove_item(item):
    if item in order:
        del order[item]
    return redirect(url_for('index'))

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
