from django.db import models

class Artwork(models.Model):
    image_path = models.TextField()  # 对应 Flask 的 image_path TEXT NOT NULL
    prompt = models.TextField()       # 对应 Flask 的 prompt TEXT NOT NULL
    parameters = models.TextField()   # 对应 Flask 的 parameters TEXT NOT NULL

    class Meta:
        db_table = "artworks"  # 保持和原表名一致（可选）
        ordering = ["-id"]

    def __str__(self):
        return f"Artwork #{self.id}: {self.prompt[:50]}"

class Favorite(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorites"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["artwork"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Favorite: Artwork #{self.artwork_id}"
