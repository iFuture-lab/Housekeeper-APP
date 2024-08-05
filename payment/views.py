from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
import json
import hashlib
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

# Corrected variable assignment
MERCHANT_PASS = 'e94b0b4a5ae7c51e99ca2fda42ad1bf1'


def compute_hash(payment_public_id, order_number, order_amount, order_currency, order_description, merchant_pass):
    # Concatenate fields to form the string
    concatenated_string = f"{payment_public_id}{order_number}{order_amount}{order_currency}{order_description}{merchant_pass}"

    # Compute MD5 hash of the concatenated string
    md5_hash = hashlib.md5(concatenated_string.encode()).hexdigest()

    # Compute SHA1 hash of the MD5 hash
    sha1_hash = hashlib.sha1(md5_hash.encode()).hexdigest().upper()

    return sha1_hash

# Example usage
payment_public_id = "hijenanaliahmedsolimn"
order_number = "2468"
order_amount = "100.00"  # Ensure this is in the correct format
order_currency = "USD"
order_description = "Order description"
merchant_pass = "e94b0b4a5ae7c51e99ca2fda42ad1bf1"

hash_value = compute_hash(payment_public_id, order_number, order_amount, order_currency, order_description, merchant_pass)
print("Computed Hash:", hash_value)




@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info('Parsed JSON data successfully.')
        except json.JSONDecodeError:
            logger.error('Invalid JSON received.')
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        action = data.get('action') or data.get('type')
        if not action:
            logger.error('Missing required field: action.')
            return JsonResponse({'error': 'Missing required field: action'}, status=400)
        
        valid_actions = dict(Payment.ACTION_CHOICES).keys()
        if action not in valid_actions:
            logger.error(f'Invalid action value: {action}.')
            return JsonResponse({'error': 'Invalid action value'}, status=400)
        
        status = data.get('status')
        if not status:
            logger.error(f'Missing required field: {status}.')
            return JsonResponse({'error': 'Missing required field: status'}, status=400)
        valid_status = dict(Payment.STATUS_CHOICES).keys()
        if status not in valid_status:
            logger.error(f'Invalid action value: {status}.')
            return JsonResponse({'error': 'Invalid status value'}, status=400)
        
        result = data.get('result','')
        # if not result:
        #     return JsonResponse({'error': 'Missing required field: result'}, status=400)
        valid_result = dict(Payment.RESULT_CHOICES).keys()
        if result not in valid_result:
            logger.error(f'Invalid result value: {status}.')
            return JsonResponse({'error': 'Invalid result value'}, status=400)
        
        if 'redirect_params' in data:
            try:
                data['redirect_params'] = json.loads(data['redirect_params'])
            except json.JSONDecodeError:
                logger.error('Invalid JSON in redirect_params.')
                return JsonResponse({'error': 'Invalid redirect_params format'}, status=400)


        # Extract common fields
        payment_public_id = data.get('payment_public_id', '')
        order_id = data.get('order_id') or data.get('order_number')
        amount = data.get('amount') or data.get('order_amount')
        if amount is None:
            amount = 0.00 
        currency = data.get('order_currency') or data.get('currency')
        if currency is None:
            currency = 'no currency'
        # Adjust as needed
        description = data.get('description') or data.get('order_description')
        hash= data.get('hash','') or data.get('')# May not be in all callbacks
        # Extract other fields
    
        trans_id = data.get('trans_id') or data.get('order_number')
        trans_date = data.get('trans_date','') 
        if trans_date:
            try:
                trans_date = datetime.strptime(trans_date, '%Y-%m-%dT%H:%M:%S')
                # trans_date = datetime.strptime(trans_date, '%Y-%m-%dT%H:%M:%S')  # Adjust the format if necessary
            except ValueError:
                logger.error('Invalid trans_date format.')
                return JsonResponse({'error': 'Invalid trans_date format. Must be in YYYY-MM-DDTHH:MM:SS format.'}, status=400)
        else:
            trans_date = None  # Handle missing date as needed, or set to a default
        descriptor = data.get('descriptor')
        recurring_token = data.get('recurring_token')
        schedule_id = data.get('schedule_id')
        card_token = data.get('card_token')
        decline_reason = data.get('decline_reason')
        redirect_url = data.get('redirect_url')
        redirect_params = data.get('redirect_params')
        redirect_method = data.get('redirect_method')
        card = data.get('card')
        card_expiration_date = data.get('card_expiration_date')
        source = data.get('source')
        
        computed_hash = compute_hash(payment_public_id, order_id, amount, currency, description, MERCHANT_PASS)

        # Validate the hash
        if hash and hash != computed_hash:
            return JsonResponse({'error': 'Invalid hash value'}, status=400)

        # Create or update the Payment record
        
        logger.info(f'Received payment data: {data}')
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
                'redirect_params': redirect_params,
                'redirect_method': redirect_method,
                'card': card,
                'card_expiration_date': card_expiration_date,
                'hash': hash,
                'source': source,
            }
        )
        
        logger.info('Payment record updated or created successfully.') 
        return JsonResponse({'success': True})
       
        
    logger.error('Invalid request method.')
    return JsonResponse({'error': 'Invalid request method'}, status=405)
