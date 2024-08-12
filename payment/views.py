from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
import json
import logging
from datetime import datetime
import base64
from django.conf import settings

logger = logging.getLogger(__name__)
LOG_FILE_PATH = settings.TEST_LOG_FILE_PATH

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type', '')
        data = None
        
        if content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))  # JSON data
                data_type = 'JSON'
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        elif content_type == 'application/x-www-form-urlencoded':
            data = request.POST.dict()  # Form data
            data_type = 'Form'
        
        elif content_type == 'text/plain':
            data = request.body.decode('utf-8')  # Plain text data
            data_type = 'Plain Text'
        
        else:
            data = request.body.decode('utf-8')  # Handle other types of data as raw bytes
            data_type = 'Raw Bytes'

        # Save raw data and type to file
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"{datetime.now()} - Data Type: {data_type}, Data: {data}\n")
        
        logger.info(f'Received {data_type} data: {data}')
        
        if data_type == 'Form':
            # Extract necessary fields from the data
            action = data.get('action') or data.get('type')
            status = data.get('status')
            result = data.get('result', '')

            redirect_params = data.get('redirect_params[body]', '')
            if redirect_params:
                try:
                    decoded_params = base64.b64decode(redirect_params).decode('utf-8')
                    json_params = json.loads(decoded_params)
                except Exception as e:
                    logger.error('Failed to decode or parse redirect_params: %s', e)
                    return JsonResponse({'error': 'Invalid redirect_params'}, status=400)
                
            payment_public_id = data.get('payment_public_id', '')
            order_id = data.get('order_id') or data.get('order_number')
            print(order_id)
            amount = float(data.get('amount') or 0.00)
            currency = data.get('order_currency') or data.get('currency') or 'no currency'
            description = data.get('description') or data.get('order_description')
            hash_value = data.get('hash', '') or ''
            trans_id = data.get('trans_id') or data.get('order_number')
            trans_date = data.get('trans_date', '')
            if trans_date:
                try:
                    trans_date = datetime.strptime(trans_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    logger.error('Invalid trans_date format.')
                    return JsonResponse({'error': 'Invalid trans_date format. Must be in YYYY-MM-DD HH:MM:SS format.'}, status=400)
            else:
                trans_date = None
            
            descriptor = data.get('descriptor')
            recurring_token = data.get('recurring_token')
            schedule_id = data.get('schedule_id')
            card_token = data.get('card_token')
            decline_reason = data.get('decline_reason')
            redirect_url = data.get('redirect_url')
            redirect_method = data.get('redirect_method')
            card = data.get('card')
            card_expiration_date = data.get('card_expiration_date')
            source = data.get('source')
        
            # Create or update the Payment record
            Payment.objects.update_or_create(
                order_id=order_id,
                defaults={
                    'action': action,
                    'result': result,
                    'status': status,
                    'trans_id': trans_id,
                    'trans_date': trans_date,
                    'descriptor': descriptor,
                    'recurring_token': recurring_token,
                    'schedule_id': schedule_id,
                    'card_token': card_token,
                    'amount': amount,
                    'currency': currency,
                    'decline_reason': decline_reason,
                    'redirect_url': redirect_url,
                    'redirect_params': json_params if redirect_params else None,
                    'redirect_method': redirect_method,
                    'card': card,
                    'card_expiration_date': card_expiration_date,
                    'hash': hash_value,
                    'source': source,
                }
            )
        
            logger.info('Payment record updated or created successfully.')
            return JsonResponse({'success': True})
        
        logger.error('Invalid request method.')
        return JsonResponse({'error': 'Invalid request method'}, status=405)
