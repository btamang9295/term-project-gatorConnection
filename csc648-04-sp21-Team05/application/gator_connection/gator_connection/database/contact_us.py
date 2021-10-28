from django.core.mail import send_mail


class ContactUs:
    """
    A class that implement ContactUs function that send the email to team from
    user and telling some thing that they need.

    **Methods:**
    - sendContactUsFormEmail(request)
    """
    @staticmethod
    def sendContactUsFormEmail(request):
        """
        This function are sending the email to team.

        :type request: int
        :param request: Should be a GET HttpRequest object that has the email information
        :return:None
        :rtype:email
        """

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        description = request.POST.get('description')

        email_content = f"""A Contact Us form has been filed. Here is what the user said:\n
First Name: {first_name}
Last Name: {last_name}
Email: {email}

Question or Issue:
{description}"""

        send_mail(
            'Contact Us Form',
            email_content,
            'Do Not Reply | Gator-connection',
            ["CSC648Team05@gmail.com"],
            fail_silently=False
        )

