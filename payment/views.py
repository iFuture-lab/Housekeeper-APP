from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
import json
import logging
from datetime import datetime
import base64
from django.conf import settings
from housekeeper.models import HireRequest,RecruitmentRequest,TransferRequest,Status

logger = logging.getLogger(__name__)
LOG_FILE_PATH = settings.TEST_LOG_FILE_PATH

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type', '')
        data = None
        
        if content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))  
                data_type = 'JSON'
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        elif content_type == 'application/x-www-form-urlencoded':
            data = request.POST.dict()  
            data_type = 'Form'
        
        elif content_type == 'text/plain':
            data = request.body.decode('utf-8')  
            data_type = 'Plain Text'
        
        else:
            data = request.body.decode('utf-8')  
            data_type = 'Raw Bytes'

        
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"{datetime.now()} - Data Type: {data_type}, Data: {data}\n")
        
        logger.info(f'Received {data_type} data: {data}')
        
        if data_type == 'Form':
            
            action = data.get('action') or data.get('type')
            status = data.get('status')
            result = data.get('result', '')
            order_id = data.get('order_id') or data.get('order_number')
            print(order_id)

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
            
            # try:
            #     hire_request = HireRequest.objects.get(order_id=order_id)
            # except HireRequest.DoesNotExist:
            #     return JsonResponse({'error': 'HireRequest not found'}, status=404)
            
            
            # hire_request = HireRequest.objects.get(order_id=order_id)
            # transfer_request = TransferRequest.objects.get(order_id=order_id)
            # recruitment_request = RecruitmentRequest.objects.get(order_id=order_id)
            
            
            
            model_mapping = {
            'hire_request': HireRequest,
            'transfer_request': TransferRequest,
            'recruitment_request': RecruitmentRequest,
        }

     
            request_obj = None
            request_model_name = None

            for model_name, model in model_mapping.items():
                try:
                    request_obj = model.objects.get(order_id=order_id)
                    request_model_name = model_name
                    break
                except model.DoesNotExist:
                    continue

            if request_obj is None:
                return JsonResponse({'error': 'Request not found'}, status=404)
            
            
        
            
            Payment.objects.update_or_create(
                order_id=order_id,
                defaults={
                    'action': action,
                    'result': result,
                    # 'hire_request': hire_request,
                    # 'transfer_request':transfer_request,
                    # 'recruitment_request':recruitment_request,
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
                    request_model_name: request_obj
                }
            )
            
            #Update the HireRequest status 
            # if hire_request:
            #     print(hire_request)
            #     if status == 'success':
            #         print("tired")
            #         hire_request.Status = 'paid'
            #         print(hire_request.Status)
                    
            #         hire_request.save()
                    
            # elif transfer_request:
            #     if status == 'success':
            #         transfer_request.status='paid' 
            #         transfer_request.save()
                    
            # elif recruitment_request:
            #     if status == 'success':
            #         recruitment_request.status='paid'
            #         recruitment_request.save()
            
            
            status_instance, created = Status.objects.get_or_create(Status='Paid')

            if request_obj:
                request_obj.status = status_instance
                request_obj.save()
            
            # if request_obj:
            #     logger.info(f'Attempting to update status to for order_id {order_id}')
                 
            #     print("tirrrrrrrrrrrrrred")
            #     request_obj.status = 'paid'
            #     print(request_obj.status)
            #     request_obj.save()
            #     print(request_obj)
            #     logger.info(f'Attempting to update status to {request_obj.status} for order_id {order_id}')
                
            # else:
            #     request_obj.Status = 'payment_failed'

            #     request_obj.save()

                
                
        
            logger.info('Payment record updated or created successfully.')
            return JsonResponse({'success': True})
        
        logger.error('Invalid request method.')
        return JsonResponse({'error': 'Invalid request method'}, status=405)
