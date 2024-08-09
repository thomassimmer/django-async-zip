'use client';

import { useToastContext } from '@/app/providers/toast-provider';
import { useUserContext } from '@/app/providers/user-provider';
import { axiosPublic } from '@/lib/axios';
import { getFileNameFromDisposition } from '@/lib/file-utils';
import FolderZipIcon from '@mui/icons-material/FolderZip';
import LoadingButton from '@mui/lab/LoadingButton';
import { Icon, Stack, Typography } from '@mui/material';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

export default function HomeConnected() {
  const { t } = useTranslation();

  const { user } = useUserContext();
  const {
    setToastCategory,
    setToastMessage,
    setToastTitle,
    setShowToast,
    setToastDuration,
  } = useToastContext();

  const [loadingZip, setLoadingZip] = useState(false);

  const handleGenerateZip = async () => {
    setLoadingZip(true);

    try {
      const response = await axiosPublic.get(
        '/api/generate-zip/',
        {
          responseType: 'blob'
        }
      );
      const fileName =
        getFileNameFromDisposition(response.headers['content-disposition']) || 'export.zip';
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');

      link.href = url;
      link.setAttribute('download', fileName);
      link.click();
    } catch (e) {
      console.error(e);

      setToastCategory('error');
      setToastTitle('Error');
      setToastDuration(3000);
      setToastMessage(`An error occured while generating the zip file.`);
      setShowToast(true);
    } finally {
      setLoadingZip(false);
    }
  };

  return (
    <Stack style={{ alignItems: 'center', justifyContent: 'center' }} py={10} spacing={5}>
      <Typography variant='h2'>
        {t('Welcome')} {user && user.username}!
      </Typography>


      <LoadingButton
        sx={{
          borderRadius: 1,
          fontFamily: 'inherit',
          width: 'fit-content',
          p: 2,
          alignItems: 'start'
        }}
        variant='outlined'
        onClick={handleGenerateZip}
        loading={loadingZip}
        startIcon={
          <Icon sx={{ display: 'flex' }}>
            <FolderZipIcon />
          </Icon>
        }
      >
        {t('Click here to download a zip file')}
      </LoadingButton>
    </Stack>
  );
}
