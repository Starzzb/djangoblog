import sqlite3
from django.core.management.base import BaseCommand
from gallery.models import Artwork, Favorite
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = "从 Flask 的 ai_gallery.db 导入数据到 Django"

    def add_arguments(self, parser):
        parser.add_argument(
            "--db",
            type=str,
            default="ai_gallery.db",
            help="Flask SQLite 数据库文件路径",
        )

    def handle(self, *args, **options):
        db_path = options["db"]
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. 导入 artworks
        try:
            cursor.execute("SELECT id, image_path, prompt, parameters FROM artworks")
            artworks = cursor.fetchall()
            self.stdout.write(f"找到 {len(artworks)} 个作品，开始导入...")

            id_mapping = {}  # 旧ID → 新对象，用于处理收藏关联

            for old_id, image_path, prompt, parameters in artworks:
                # 检查是否已存在（避免重复导入）
                # 这里简单处理，如果已经有了就不再导入，或者清空表重新导入
                # 但考虑到这是迁移，通常是一次性的。
                artwork = Artwork.objects.create(
                    image_path=image_path,
                    prompt=prompt,
                    parameters=parameters,
                )
                id_mapping[old_id] = artwork
            
            self.stdout.write(self.style.SUCCESS(f"✅ 成功导入 {len(artworks)} 个作品"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"导入 artworks 失败: {e}"))
            return

        # 2. 导入 favorites
        try:
            cursor.execute("SELECT artwork_id, created_at FROM favorites")
            favorites = cursor.fetchall()
            self.stdout.write(f"找到 {len(favorites)} 条收藏记录，开始导入...")

            imported_fav_count = 0
            for artwork_id, created_at in favorites:
                if artwork_id in id_mapping:
                    fav = Favorite.objects.create(
                        artwork=id_mapping[artwork_id],
                    )
                    fav.created_at = created_at
                    fav.save()
                    imported_fav_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️ 跳过收藏：artwork_id={artwork_id} 不存在")
                    )

            self.stdout.write(self.style.SUCCESS(f"✅ 成功导入 {imported_fav_count} 条收藏"))
        except Exception as e:
             self.stdout.write(self.style.ERROR(f"导入 favorites 失败或者没有相关表: {e}"))

        conn.close()
        self.stdout.write(self.style.SUCCESS("🎉 数据迁移完成！"))
