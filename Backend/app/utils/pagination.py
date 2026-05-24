def paginate(query, page: int = 1, size: int = 10):
    total = query.count()

    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }