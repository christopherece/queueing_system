from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw



# Create your models here.
class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.name)
            qr.make(fit=True)
            
            # Create QR code image
            qrcode_img = qr.make_image(fill_color="black", back_color="white")
            qrcode_img = qrcode_img.resize((370, 370))
            
            # Create canvas
            canvas = Image.new('RGB', (370, 370), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img, (0, 0))
            
            # Generate filename
            fname = f'qr_code-{self.name}.png'
            
            # Save to buffer
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            
            # Save to model
            self.qr_code.save(fname, File(buffer), save=False)
            
            # Clean up
            canvas.close()
            
        except Exception as e:
            print(f"Error generating QR code: {str(e)}")
            # If QR code generation fails, still save the model
            pass
        
        super().save(*args, **kwargs)
