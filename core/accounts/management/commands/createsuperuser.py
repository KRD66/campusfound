from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    """
    Custom createsuperuser command that skips the username prompt.
    Works with email-based users where username = None.
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)
        # Remove the username argument completely
        for action in parser._actions[:]:
            if action.dest == 'username':
                parser._actions.remove(action)
                break

    def handle(self, *args, **options):
        # Make sure we don't pass username to create_superuser
        options.pop('username', None)

        # Force the email to be used as the identifier
        email = options.get('email')
        if not email:
            email = input("Email address: ").strip()
            options['email'] = email

        # Call the original handler
        try:
            super().handle(*args, **options)
        except TypeError as e:
            if 'username' in str(e):
                # Re-try without username
                user_data = {
                    'email': options['email'],
                    'password': options.get('password'),
                }
                if not user_data['password']:
                    while True:
                        password = input("Password: ")
                        password_confirm = input("Password (again): ")
                        if password == password_confirm:
                            user_data['password'] = password
                            break
                        self.stderr.write("Passwords do not match.")

                self.UserModel._default_manager.create_superuser(**user_data)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{email}" created successfully.'))
            else:
                raise