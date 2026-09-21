from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product

def get_similar_products(product_id, top_n=3):
    """
    FR-6: AI Product Recommendation
    يحسب نسبة التشابه بين المنتجات بناءً على الوصف والاسم والفئة
    ويولد تفسيراً لسبب الاقتراح
    """
    products = list(Product.objects.all())
    
    # لو عدد المنتجات قليل جداً
    if len(products) <= 1:
        return []

    # تجميع نصوص المنتجات لتحليلها
    docs = [f"{p.name} {p.description} {p.category.name}" for p in products]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(docs)
    
    # تحديد مكان المنتج الحالي
    target_idx = next(i for i, p in enumerate(products) if p.id == product_id)
    
    # حساب درجات التشابه
    scores = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()
    
    # ترتيب المنتجات تنازلياً حسب التشابه واستبعاد المنتج نفسه
    similar_indices = scores.argsort()[::-1]
    
    recommendations = []
    for idx in similar_indices:
        if products[idx].id != product_id and scores[idx] > 0:
            recommendations.append({
                'product': products[idx],
                'explanation': f"Recommended because it shares {scores[idx]*100:.0f}% feature similarity with {products[target_idx].name} in {products[idx].category.name} category."
            })
            if len(recommendations) >= top_n:
                break
                
    return recommendations