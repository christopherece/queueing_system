import os
import sys
import django

# Add project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dockinnqueue.settings')

django.setup()

from django.conf import settings

print("Checking media directory setup...")

# Check media root exists
media_root = settings.MEDIA_ROOT
print(f"Media root: {media_root}")

if not os.path.exists(media_root):
    print("Creating media root directory...")
    os.makedirs(media_root)

# Check qr_codes directory exists
qr_codes_dir = os.path.join(media_root, 'qr_codes')
print(f"QR codes directory: {qr_codes_dir}")

if not os.path.exists(qr_codes_dir):
    print("Creating qr_codes directory...")
    os.makedirs(qr_codes_dir)

# Check permissions
print("\nChecking permissions:")
print(f"Media root permissions: {oct(os.stat(media_root).st_mode)[-3:]}")
print(f"QR codes directory permissions: {oct(os.stat(qr_codes_dir).st_mode)[-3:]}")
