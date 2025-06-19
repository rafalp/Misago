def anonymize_post_last_likes(user, post):
    cleaned_likes = []
    for like in post.last_likes:
        if like["id"] == user.id:
            cleaned_likes.append({"id": None, "username": user.username})
        else:
            cleaned_likes.append(like)

    if cleaned_likes != post.last_likes:
        post.last_likes = cleaned_likes
        post.save(update_fields=["last_likes"])
