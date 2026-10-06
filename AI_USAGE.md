# AI Usage Documentation

## 1. Purpose

AI assistance was used during the development of this Django-based AI-Assisted Box Selection System as a development and learning aid.

The AI assistance was primarily used for reviewing implementation approaches, explaining Django concepts, suggesting frontend changes, debugging, testing guidance, and helping structure the final documentation.

The actual conversation used during the assignment is being provided separately as the AI conversation transcript/reference.

---

## 2. AI Tool Used

* Tool: ChatGPT
* Model: GPT-5.6 Luna

The AI was used interactively during development. Suggestions were reviewed and tested in the actual project before being accepted.

---

## 3. How AI Was Used

### 3.1 Frontend development

AI assistance was used to help improve and connect the frontend templates and JavaScript to the Django application.

The conversation included work on:

* `base.html`
* `dashboard.html`
* `shop.html`
* `order_detail.html`
* `packaging.html`
* `package_qr.html`
* Frontend CSS and JavaScript files

For example, AI suggested changes to make the dashboard display database-driven values instead of static values, including total orders, pending orders, product count, and average order weight.

The suggested frontend changes were reviewed and integrated into the project.

### 3.2 Connecting the frontend to Django

AI assistance was used to identify remaining integration points between the frontend and backend.

One important point identified in the conversation was that the Shop page initially had a frontend-only cart and that the "Create Order" action needed to actually save an `Order` and `OrderItem` records in Django.

The AI suggested a Django POST-based approach using:

* CSRF protection
* Customer name and address fields
* Selected product IDs
* Product quantities
* Django `Order` creation
* Django `OrderItem` creation
* Redirecting to the order details page

The implementation was tested by me in the actual project.

### 3.3 Order list

AI suggested using the existing `/order/` route to support two states:

* `/order/` for displaying the order list
* `/order/?order=...` for displaying a specific order

This avoided unnecessarily creating another route.

The suggested implementation was tested against the actual Django database.

### 3.4 Packaging logic

The conversation included discussion and review of the packaging logic.

The implemented logic includes:

* Calculating total order weight
* Checking whether a product fits inside a box
* Allowing dimensional rotation when checking fit
* Selecting the cheapest suitable box for a single-package order
* Splitting products into multiple boxes using a simplified greedy approach

The AI explicitly identified that the multi-box approach is a simplified volume-based/greedy approach rather than a complete three-dimensional bin-packing algorithm.

I verified the packaging functions manually in Django's shell using test cases including:

1. Calculating order weight
2. Checking whether the charger fits in the small box
3. Checking that the monitor does not fit in the small box
4. Checking the best-box selection
5. Checking multi-box packaging

These tests were personally run and verified in the project.

### 3.5 Testing guidance

After the application was completed, AI assistance was used to create a manual end-to-end testing checklist.

The suggested workflow was:

```text
Shop
↓
Create Order
↓
Order List
↓
Order Details
↓
Packaging
↓
Package QR
```

The application was then tested by me, and I confirmed that the complete workflow was working.

The testing guidance also included checking:

* Django system checks
* Django tests
* Database records
* Order creation
* Order items
* Packaging recommendations
* No suitable package cases
* Invalid order cases
* Browser console errors
* Responsive layout
* Removal of hardcoded/mock frontend data

---

## 4. Suggestions I Accepted

The following suggestions from the AI were accepted and incorporated into the development process:

* Using Django's SQLite database for the application data.
* Using Django models for `Product`, `Box`, `Order`, and `OrderItem`.
* Making dashboard information database-driven.
* Making the product page use products from the Django database rather than hardcoded frontend products.
* Making the order page display actual Django orders.
* Connecting order creation to Django rather than leaving it as a JavaScript-only operation.
* Using the existing `/order/` URL for both the order list and individual order details.
* Using Django's packaging functions to generate package recommendations.
* Testing the packaging functions individually before testing the complete application.
* Performing an end-to-end test of the complete application before documentation.

---

## 5. Suggestions I Modified

Some suggestions were treated as implementation guidance rather than copied unchanged.

The frontend and backend code was adapted to the existing project structure and implementation.

In particular:

* The frontend suggestions were fitted into the existing Django templates and static-file structure.
* The existing models and packaging functions were retained and worked with rather than replacing the project with a different architecture.
* The Package QR implementation was not taken directly from the AI suggestions. I used code from my previous projects to make the QR functionality work.
* Testing was performed against the actual implementation rather than assuming that suggested code would work without verification.

---

## 6. Suggestions I Rejected or Did Not Use

The AI suggested additional improvements and possible future features during the conversation. These were not treated as requirements for the assignment.

I intentionally did not add unnecessary features after the core application was working.

Examples of features that were not pursued included additional advanced functionality such as authentication, payments, Docker, PostgreSQL, React, or other unrelated enhancements.

The goal was to keep the assignment focused on the required Django warehouse and packaging workflow.

---

## 7. Problems Personally Verified

AI-generated or suggested code was not treated as automatically correct.

I personally ran and verified the implementation in the Django project.

Examples of verification included:

### Packaging logic

I tested:

* `get_order_weight()`
* `product_fits()`
* `get_best_box()`
* `get_multi_box_packaging()`

The results were inspected using Django's shell.

### Database

I verified that the actual products, boxes, orders, and order items were stored in and retrieved from the Django SQLite database.

### Frontend

I manually tested the pages and their interactions, including:

* Dashboard
* Shop
* Order List
* Order Details
* Packaging
* Package QR

### Complete workflow

I personally tested the complete application flow:

```text
Product selection
→
Create Order
→
Order saved
→
Order List
→
Order Details
→
Packaging
→
Package QR
```

The complete workflow was working before moving to the documentation stage.

---

## 8. AI Assistance vs. My Verification

AI assistance was used for suggestions, explanations, implementation guidance, debugging, and testing guidance.

However, the suggestions were not considered proof that the application worked.

I was responsible for:

* Applying the changes to my project
* Running the Django application
* Entering and verifying database data
* Testing the packaging functions
* Testing the frontend workflow
* Testing order creation
* Testing the packaging workflow
* Testing the QR functionality
* Verifying that the final application worked

The final implementation was therefore verified against the actual running application rather than being accepted solely based on AI output.

---

## 9. Limitations of the Packaging Algorithm

The packaging algorithm was also discussed during the AI-assisted development process.

The multi-box implementation uses a simplified greedy approach based on:

* Product weight
* Box maximum weight
* Individual product dimensions
* Total product volume
* Box volume

It does not attempt to solve a mathematically optimal three-dimensional bin-packing problem.

This limitation is understood and was kept within the scope of the assignment.

---

## 10. Transparency

This document is intended to accurately describe how AI assistance was used during the assignment.

The accompanying AI conversation provides the detailed interaction and context for the assistance described here.

No claim is made that AI was not used. AI assistance was used as a development and learning aid, while the resulting code and application were tested in the actual project before completion.
