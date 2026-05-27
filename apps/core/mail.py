import quopri
from django.core.mail.backends.console import EmailBackend as BaseConsoleBackend


class ConsoleEmailBackend(BaseConsoleBackend):
    """Backend de consola que decodifica quoted-printable para que las URLs sean copiables."""

    def write_message(self, message):
        msg = message.message()
        msg_str = msg.as_string()

        if 'Content-Transfer-Encoding: quoted-printable' in msg_str:
            headers, _, body = msg_str.partition('\n\n')
            body_decoded = quopri.decodestring(body.encode()).decode('utf-8', errors='replace')
            msg_str = headers + '\n\n' + body_decoded

        self.stream.write('%s\n' % msg_str)
        self.stream.write('-' * 79)
        self.stream.write('\n')
        self.stream.flush()
