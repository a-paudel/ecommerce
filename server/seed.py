import io
import os
from pathlib import Path
from pydoc import describe
import django
from django.core.management import call_command
from django.conf import settings
from django.core.files.images import ImageFile
from django.apps import apps
import secrets
import random
import faker
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from store.models import Category, Product, ProductImage

if not settings.DEBUG:
    print("The DEBUG option is not enabled.")
    sys.exit(1)

for model in apps.get_app_config("store").get_models():
    model.objects.all().delete()

random.seed(0)
faker.Faker.seed(0)

fake = faker.Faker()

# create 5 categories
for _ in range(5):
    Category.objects.create(name=fake.word(), description=fake.paragraph())


categories = Category.objects.all()


# def get_product_name():
#     name = fake.word()
#     is_exists = Product.objects.filter(name=name).exists()
#     if is_exists:
#         return get_product_name()
#     return name


# create 50 products
for _ in range(50):
    Product.objects.create(
        name=fake.word(),
        description=fake.paragraph(),
        # between 0 and 5 tags
        tags="\n".join(fake.words(nb=random.randint(0, 5))),
        base_price=random.random() * 100,
        stock=random.randint(0, 100),
        category=random.choice(categories),
    )

products = Product.objects.all()
# create 100 images
for _ in range(100):
    image = fake.image()
    # file_path = Path(f"/app/media/product_images/{secrets.token_hex()}.png")
    # file_path.parent.mkdir(parents=True, exist_ok=True)
    # save to media/product_images folder
    # file_path.write_bytes(image)
    ProductImage.objects.create(
        product=random.choice(products),
        image=ImageFile(file=io.BytesIO(image), name=f"{secrets.token_hex()}.png"),
    )
