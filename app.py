from flask import Flask, render_template, request, redirect
app = Flask(__name__)


items = [
    {"id": 1, "name": "White Coffee Mug", "imagefile":"images/image1.jpg", "price": 11.99, "rating": 4.3},
    {"id": 2, "name": "Black Backpack", "imagefile":"images/image2.jpg", "price": 69.99, "rating": 4.2},
    {"id": 3, "name": "Red/Black Paper Bag", "imagefile":"images/image3.jpg", "price": 6.99, "rating": 4.9},
    {"id": 4, "name": "Notebook (200pg.)", "imagefile":"images/image4.jpg", "price": 10.99, "rating": 4.1},
    {"id": 5, "name": "White Analog Alarm Clock", "imagefile":"images/image5.jpg", "price": 14.49, "rating": 3.9},
    {"id": 6, "name": "600mL Tumbler", "imagefile":"images/image6.jpg", "price": 8.49, "rating": 4.6}
]

cart_name_list = [] 
cart_cost_list = []
cart_other_info = []
@app.route("/")
def index():
    return render_template("index.html", items=items)

@app.route("/details/<item_num>", methods=["GET", "POST"])
def detail(item_num):
    details = items[int(item_num)-1]
    other_detail = []
    if request.method == "POST":
        selected_shipping = request.form["shipping"]
        quantity = int(request.form['quantity'])
        other_detail.append(quantity)
        cost_per_product = details['price']
        if selected_shipping == "1-2 days later: $7":
            shipping_cost = 7
            other_detail.append(7)
        if selected_shipping == "4-5 days later: $4":
            shipping_cost = 4
            other_detail.append(4)
        if selected_shipping == "+7 days later: Free shipping":
            shipping_cost = 0
            other_detail.append(0)
        total_cost = int((cost_per_product * quantity + shipping_cost) * 100) / 100
        cart_cost_list.append(total_cost)
        cart_name_list.append(details)
        cart_other_info.append(other_detail)
        return redirect('/cart')
    return render_template('item-detail.html', details=details)

@app.route('/cart')
def cart():
    cost_sum = sum(cart_cost_list)
    return render_template("cart.html", cart_name_list=cart_name_list, cart_cost_list=cart_cost_list, cart_other_info=cart_other_info, length=len(cart_name_list), cost_sum = cost_sum)

@app.route('/remove/<int:index>')
def remove(index):
    global cart_name_list, cart_cost_list, cart_other_info

    cart_name_list.pop(index)
    cart_cost_list.pop(index)
    cart_other_info.pop(index)

    return redirect("/cart")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)