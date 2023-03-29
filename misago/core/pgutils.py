def chunk_queryset(queryset, chunk_size=20):
    ordered_queryset = queryset.order_by("-pk")  # bias to newest items first
    return ordered_queryset.iterator(chunk_size=chunk_size)
