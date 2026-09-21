# API & AI Documentation

## 1. Add to Cart API
- **Endpoint:** `/api/cart/add/<int:product_id>/`
- **Method:** `POST`
- **Description:** Adds a product to the authenticated user's cart using Vanilla JS.
- **Request Headers:**
  - `X-CSRFToken`: Django CSRF Token
  - `Content-Type`: application/json
- **Response Example:**
  ```json
  {
    "status": "success",
    "total_items": 2
  }
  ## 2. AI Product Recommendation Engine
* **Methodology:** Content-Based Filtering using TF-IDF Vectorization & Cosine Similarity.
* **Feature Inputs:** Product Name, Category Name, and Description.
* **Outputs:** Top 3 similar products along with an explainability rationale.