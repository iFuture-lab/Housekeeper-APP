from django.db import models
import uuid
from django.utils import timezone
from django.core.files.base import ContentFile
import base64
from django.core.exceptions import ValidationError

# Create your models here.

##################soft###################################

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        #  filters out soft-deleted records
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        # Return only soft-deleted records
        return super().get_queryset().filter(deleted_at__isnull=False)

    def with_deleted(self):
        # all the records 
        return super().get_queryset()
    
    
    
class Nationallity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Nationality= models.CharField(max_length=150,unique=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='nationality_images/', null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    
    def save_image_from_base64(self, base64_image_data, filename):
        """Save image from base64 string."""
        if base64_image_data:
            format, imgstr = base64_image_data.split(';base64,') 
            ext = format.split('/')[-1]  
            self.image.save(f'{filename}.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)
            
            
    def save(self, *args, **kwargs):
        # Normalize to lowercase before saving
        self.Nationality = self.Nationality.lower()
        super().save(*args, **kwargs)
    
    # def save_image_from_base64(self, base64_image_data, filename):
    #     if base64_image_data:
    #         try:
    #             # Check if the base64 string starts with the correct prefix
    #             if not base64_image_data.startswith('data:image/'):
    #                 raise ValidationError('Base64 string does not start with "data:image/".')

    #             # Split the base64 string to extract the format and the image data
    #             format, imgstr = base64_image_data.split(';base64,') 
                
    #             # Extract the file extension from the format
    #             ext = format.split('/')[-1]
                
    #             # print(f'Base64 string before padding: {imgstr}')
                
    #             # missing_padding = len(imgstr) % 4
    #             # if missing_padding != 0:
    #             #     imgstr += '=' * (4 - missing_padding)
                    
    #             decoded_file = base64.b64decode(imgstr)    
                
    #             # Create a ContentFile object
    #             content_file = ContentFile(decoded_file, name=f'{filename}.{ext}')
                
    #             # Save the image file
    #             self.image.save(content_file.name, content_file, save=False)
    #         except (TypeError, base64.binascii.Error) as e:
    #             raise ValidationError(f'Invalid base64-encoded string: {e}')
    #         except Exception as e:
    #             raise ValidationError(f'An unexpected error occurred: {e}')
    
    
    
    objects = SoftDeleteManager()  
    all_objects = models.Manager()  

    def delete(self):
       #soft deleting
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # Restore a soft-deleted record 
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        # delete the record in real 
        super().delete()

   
    def __str__(self):
        return self.Nationality
 