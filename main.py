from manager import Manager
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

manager = Manager()

@app.route('/')
def home():
    state = manager.state
    return render_template('home.html', state=state)

@app.route('/purchase', methods=['POST'])
def purchase():
    product_name = request.form['product_name']
    unit_price = int(request.form['unit_price'])
    number_of_pieces = int(request.form['number_of_pieces'])

    if unit_price <= 0 or number_of_pieces <= 0:
        flash('Unit price and number of pieces must be greater than zero.')
        return redirect(url_for('home'))

    cost = unit_price * number_of_pieces
    if manager.state['caly_stan'] < cost:
        flash('Insufficient balance to make the purchase.')
        return redirect(url_for('home'))

    manager.state['cena_produktow'][product_name] = unit_price
    manager.state['slownik_produktow'][product_name] = manager.state['slownik_produktow'].get(product_name, 0) + number_of_pieces
    manager.state['caly_stan'] -= cost
    manager.state['historia'].append(['zakup', product_name, number_of_pieces])
    manager.save_state()
    return redirect(url_for('home'))

@app.route('/sale', methods=['POST'])
def sale():
    product_name = request.form['product_name']
    number_of_pieces = int(request.form['number_of_pieces'])

    if product_name not in manager.state['slownik_produktow']:
        flash('Product does not exist.')
        return redirect(url_for('home'))

    if number_of_pieces <= 0:
        flash('Number of pieces must be greater than zero.')
        return redirect(url_for('home'))

    if manager.state['slownik_produktow'][product_name] < number_of_pieces:
        flash('Insufficient stock to make the sale.')
        return redirect(url_for('home'))

    unit_price = manager.state['cena_produktow'][product_name]
    revenue = unit_price * number_of_pieces
    manager.state['slownik_produktow'][product_name] -= number_of_pieces
    manager.state['caly_stan'] += revenue
    manager.state['historia'].append(['sprzedaz', product_name, number_of_pieces])
    manager.save_state()
    return redirect(url_for('home'))

@app.route('/balance_change', methods=['POST'])
def balance_change():
    comment = request.form['comment']
    value = int(request.form['value'])

    if value == 0:
        flash('Value must be different from zero.')
        return redirect(url_for('home'))

    if manager.state['caly_stan'] + value < 0:
        flash('Insufficient balance for this operation.')
        return redirect(url_for('home'))

    manager.state['caly_stan'] += value
    manager.state['historia'].append(['saldo', comment, value])
    manager.save_state()
    return redirect(url_for('home'))

@app.route('/history/')
@app.route('/history/<int:line_from>/<int:line_to>/')
def history(line_from=0, line_to=None):
    history = manager.state['historia']
    if line_to is None:
        line_to = len(history)
    return render_template('history.html', history=history[line_from:line_to])

if __name__ == "__main__":
    app.run(debug=True)
