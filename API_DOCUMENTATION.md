# API Documentation

## 1. Cart Management

### Add Product to Cart
- **Endpoint:** `/api/cart/add/<int:product_id>/`
- **Method:** `POST`
- **Description:** Adds a specific product to the user's active shopping cart.
- **Response:**
  ```json
  {
    "status": "success",
    "total_items": 1
  }
