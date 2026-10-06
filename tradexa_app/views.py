from django.shortcuts import render, redirect
from .models import Product, Box, Order, OrderItem
import qrcode
import base64
from io import BytesIO

def dashboard(request):
    orders = Order.objects.all().order_by("-created_at")

    total_orders = orders.count()
    pending_orders = orders.filter(status="pending").count()
    total_products = Product.objects.count()

    total_weight = 0

    for order in orders:
        total_weight += get_order_weight(order)

    average_weight = 0

    if total_orders > 0:
        average_weight = total_weight / total_orders

    return render(
        request,
        "tradexa_app/dashboard.html",
        {
            "orders": orders[:5],
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "total_products": total_products,
            "average_weight": average_weight,
        }
    )


def shop(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        address = request.POST.get("address")
        product_ids = request.POST.getlist("product_id")
        last_order = Order.objects.order_by("-id").first()
        if last_order:
            number = int(last_order.order_number.split("-")[1]) + 1
        else:
            number = 1001
        order_number = f"ORD-{number}"
        order = Order.objects.create(
            order_number=order_number,
            customer_name=customer_name,
            address=address,
            status="pending"
        )
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            quantity = int(
                request.POST.get(
                    f"quantity_{product_id}",
                    1
                )
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                qty=quantity
            )

        return redirect(
            f"/order/?order={order.order_number}"
        )
    products = Product.objects.all().order_by("name")

    return render(
        request,
        "tradexa_app/shop.html",
        {
            "products": products
        }
    )

def order_detail(request):
    order_number = request.GET.get("order")

    if not order_number:
        orders = Order.objects.all().order_by("-created_at")

        return render(
            request,
            "tradexa_app/order_detail.html",
            {
                "orders": orders,
            }
        )

    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        order = None

    total_weight = None

    if order:
        total_weight = get_order_weight(order)

    return render(
        request,
        "tradexa_app/order_detail.html",
        {
            "order": order,
            "total_weight": total_weight,
        }
    )

def packaging(request):
    order_number = request.GET.get("order")

    order = None
    packages = None
    order_weight = None

    if order_number:
        try:
            order = Order.objects.get(order_number=order_number)
            order_weight = get_order_weight(order)
            packages = get_multi_box_packaging(order)
        except Order.DoesNotExist:
            order = None

    return render(
        request,
        "tradexa_app/packaging.html",
        {
            "order": order,
            "packages": packages,
            "order_weight": order_weight,
        }
    )


def package_qr(request):
    order_number = request.GET.get("order")
    order = None
    qr_code = None
    if order_number:
        try:
            order = Order.objects.get(
                order_number=order_number
            )
            qr_text = (
                f"Order: {order.order_number}\n"
                f"Customer: {order.customer_name}\n"
                f"Address: {order.address}"
            )
            qr = qrcode.make(qr_text)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            qr_code = base64.b64encode(
                buffer.getvalue()
            ).decode()
        except Order.DoesNotExist:
            order = None
    return render(
        request,
        "tradexa_app/package_qr.html",
        {
            "order": order,
            "qr_code": qr_code
        }
    )

def get_order_weight(order):
    total_weight = 0
    for item in order.items.all():
        total_weight += item.product.weight * item.qty

    return total_weight

def product_fits(product, box):
    product_dimensions = [
        product.length,
        product.width,
        product.height
    ]

    box_dimensions = [
        box.length,
        box.width,
        box.height
    ]

    product_dimensions.sort()
    box_dimensions.sort()
    for i in range(3):
        if product_dimensions[i] > box_dimensions[i]:
            return False

    return True

def get_best_box(order):
    total_weight = get_order_weight(order)
    boxes = Box.objects.all()
    suitable_boxes = []
    for box in boxes:
        if total_weight > box.max_weight:
            continue
        fits = True
        for item in order.items.all():
            if not product_fits(item.product, box):
                fits = False
                break

        if fits:
            suitable_boxes.append(box)
    if len(suitable_boxes) == 0:
        return None

    best_box = suitable_boxes[0]
    for box in suitable_boxes:
        if box.cost < best_box.cost:
            best_box = box

    return best_box

def can_add_item_to_box(item, box, current_items):
    current_weight = 0
    current_volume = 0
    for current_item in current_items:
        current_weight += current_item.product.weight
        current_volume += (
            current_item.product.length *
            current_item.product.width *
            current_item.product.height
        )
    item_weight = item.product.weight
    item_volume = (
        item.product.length *
        item.product.width *
        item.product.height
    )
    total_weight = current_weight + item_weight
    total_volume = current_volume + item_volume

    if total_weight > box.max_weight:
        return False
    if not product_fits(item.product, box):
        return False
    box_volume = box.length * box.width * box.height
    if total_volume > box_volume:
        return False

    return True

def get_multi_box_packaging(order):
    items = []
    for item in order.items.all():
        for i in range(item.qty):
            items.append(item)

    items.sort(
        key=lambda item: item.product.weight,
        reverse=True
    )
    boxes = Box.objects.all().order_by("cost")

    packages = []
    
    for item in items:
        item_added = False
        for package in packages:
            box = package["box"]
            current_items = package["items"]

            if can_add_item_to_box(item, box, current_items):
                package["items"].append(item)
                item_added = True
                break
        if item_added:
            continue
        for box in boxes:
            if can_add_item_to_box(item, box, []):
                new_package = {
                    "box": box,
                    "items": [item]
                }
                packages.append(new_package)
                item_added = True
                break
        if not item_added:
            return None

    return packages