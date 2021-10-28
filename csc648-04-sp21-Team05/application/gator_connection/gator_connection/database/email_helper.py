from django.core.mail import EmailMultiAlternatives


class EmailHelper:
    """
    A class that help the system implement the multiple function that base on
    send email. Such as send notification, help user located their post, verify
    the email that user register.

    **Methods:**
    - send_email(sfsu_email, first_name, code, type)

    """
    @staticmethod
    def send_email(sfsu_email, first_name, code, type):
        """
        This function are managing email sending.

        :type sfsu_email，first_name，code: str
        :type type: int
        :param sfsu_email，first_name，code, type: the elements of email information.
        :rtype:email
        """
        subject = ''
        text_content = ''''''
        html_content = ''''''

        if type == 1:
            subject = 'Thank you for your register'
            text_content = ''''''
            html_content = '''<p>Dear {},</p>
            <p>Thanks for registering with Gator Connection. Gator Connection is a one stop for all your gator needs.</p>
            <p>Please verify your email to access all of Gator Connection's features.</p>
            <p>Click below to verify email:</p>
            <a href="https://www.gator-connection.com/confirm?code={}" target=blue>Gator-Connection | Verify Email</a>.
            <br />
            <p>If you did not register with Gator Connection, please ignore this email.</p>
            <br />
            <p>Best,</p>
            <p>The Gator Connection Team</p>'''.format(first_name, code)

        if type == 2:
            housing_num = code  # here can request the housing_id
            subject = 'Your housing listing posted'
            text_content = ''''''
            html_content = '''<p>Dear {},</p>
            <p>You post a new housing listing</p>
            <p>Let's go to check it now <a href="https://www.gator-connection.com/housing/{}" target=blue>Gator-Connection</a>.</p>
            <p>Best,</p>
            <p>The Gator Connection Team</p>'''.format(first_name, housing_num)

        if type == 3:
            subject = 'New announcement'
            text_content = ''''''
            html_content = '''<p>Dear {},</p>
            <p>Your organization post a new announcement.</p>
            <p>Let's go to check it now <a href="https://www.gator-connection.com/announcements" target=blue>Gator-Connection</a>.</p>
            <p>Best,</p>
            <p>The Gator Connection Team</p>'''.format(first_name)

        if type == 4:
            item_num = code  # here can request the housing_id
            subject = 'Your item listing posted!'
            text_content = ''''''
            html_content = '''<p>Dear {},</p>
            <p>You posted a new item.</p>
            <p>Here's are you item list <a href="https://www.gator-connection.com/item/{}" target=blue>Gator-Connection</a>.</p>
            <p>Best,</p>
            <p>The Gator Connection Team</p>'''.format(first_name, item_num)

        if type == 5:
            subject = 'New Device Detected'
            text_content = ''''''
            html_content = f'''<p>Dear {first_name}, </p> <p>A new device has just logged into your account. We are 
            confirming that this is you. If not, please fill out a <a 
            href="https://www.gator-connection.com/contact">contact us form</a> so we can handle the problem 
            immediately.</p> <p>Best, </p> <p>The Gator Connection Team '''

        msg = EmailMultiAlternatives(subject, text_content, 'Gator Connection <CSC648Team05@gmail.com>', [sfsu_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
