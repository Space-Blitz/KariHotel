

from pyfcm import FCMNotification

from constants import API_KEY as key


push_service = FCMNotification(api_key=key)

class Notifications():
    """
    Send notifications
    """

    @staticmethod
    async def send_notifications(tokens, title, body, data={}):
        """
        send notifications to multiple users
        params: 
            tokens (list, optional): FCM device registration IDs
            body (str, optional): Message string to display in the notification tray
            title (str, optional): Message title to display in the notification tray
            data (str, optional): Any data that could be used byt the app, e.g. for redirection
        returns: n/a
        """
        try:
            await asyncio.sleep(1)
            push_service.notify_multiple_devices(
                registration_ids=tokens, 
                message_title=title, 
                message_body=body,
                data_message=data
            )
        except Exception as error:

            print('Notification not sent')
            print('\n')
            print(str(error))
            print('\n')


    @staticmethod
    async def send_notification(token, title, body, data={}):
        """
        send notification to a user
        params: 
            token (str): FCM device registration ID
            body (str): Message string to display in the notification tray
            title (str): Message title to display in the notification tray
            data (str): Any data that could be used byt the app, e.g. for redirection
        returns: n/a
        """
        try:
            await asyncio.sleep(1)
            print('second time')
            # push_service.notify_single_device(
            #     registration_id=token, 
            #     message_title=title, 
            #     message_body=body,
            #     data_message=data
            # )
        except Exception as error:

            print('Notification not sent')
            print('\n')
            print(str(error))
            print('\n')

