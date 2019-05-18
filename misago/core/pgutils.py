def chunk_queryset(queryset, chunk_size=20):
    ordered_queryset = queryset.order_by("-pk")  # bias to newest items first
    chunk = ordered_queryset[:chunk_size]
    while chunk:
        last_pk = None
        for item in chunk:
            last_pk = item.pk
            yield item
        chunk = ordered_queryset.filter(pk__lt=last_pk)[:chunk_size]
