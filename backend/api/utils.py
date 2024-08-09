import asyncio
import datetime
import os
from collections.abc import AsyncGenerator
from datetime import datetime
from io import BytesIO
from stat import S_IFREG

import aiofiles
from allauth.account.utils import user_pk_to_url_str
from asgiref.sync import sync_to_async
from django.conf import settings
from django.urls import reverse
from stream_zip import NO_COMPRESSION_64, ZIP_64, async_stream_zip
from xlsxwriter import Workbook

from api.models import User


def password_reset_url_generator(request, user, temp_key):
    path = reverse(
        'password_reset_confirm',
        args=[user_pk_to_url_str(user), temp_key],
    )

    return settings.FRONTEND_HOST + path


async def generate_zip() -> AsyncGenerator[bytes]:
    """
    This function generates a zip and starting sending to client chunk by chunk
    as soon as it's being created.

    The zip file contains :
    -   a folder per user with 3 files inside
    -   a excel that contains all users

    It's just an example to show how blocking operations can be processed.
    """
    excel_buffer = BytesIO()

    workbook = Workbook(excel_buffer)
    sheet = workbook.add_worksheet()

    async def generate_files_to_add_in_zip(debug=False):

        modified_at = datetime.now()
        mode = S_IFREG | 0o600

        users = await sync_to_async(list)(User.objects.all())

        user: User
        for i, user in enumerate(users):

            sheet.write_row(i, 1, [user.username, user.email])

            files = [
                'assets/example.txt'
                for _ in range(3 if settings.IS_TESTING else 100)
            ]

            for file in files:
                filename = file.split('/')[1]

                archive_path = f"{user.username}/{filename}"

                async def file_content_iterator():
                    async with aiofiles.open(os.path.join(settings.BASE_DIR, 'api', file), 'rb') as f:
                        while True:
                            chunk = await f.read(65536)
                            if not chunk:
                                break
                            if debug:
                                print(len(chunk), "sent.")
                            yield chunk

                yield (archive_path, modified_at, mode, NO_COMPRESSION_64, file_content_iterator())

                # Uncomment this to see even more the effect of a blocking
                # operation when you download the zip.
                # await asyncio.sleep(1)

        workbook.close()

        async def excel_content_iterator():
            data = excel_buffer.getvalue()
            if debug:
                print(len(data), "sent.")
            yield data

        yield ('summary.xlsx', modified_at, mode, NO_COMPRESSION_64, excel_content_iterator())

    zipped_chunks = async_stream_zip(generate_files_to_add_in_zip(debug=False))

    async for zipped_chunk in zipped_chunks:
        yield zipped_chunk
