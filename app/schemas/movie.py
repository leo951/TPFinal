def movieEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "director": item["director"],
        "actor": item["actor"],
        "duration": item["duration"]
    }

def moviesEntity(entity) -> list:
    return [movieEntity(item) for item in entity]