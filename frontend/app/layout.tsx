import './style.css';

import { i18nConfig } from './i18nConfig';

export const metadata = {
  title: 'DjangoAsyncZip',
  description: '',
  metadataBase: new URL('https://django-async-zip.com'),
};

interface RootLayoutProps {
  children: React.ReactNode;
  params: { locale: string };
}

export function generateStaticParams() {
  return i18nConfig.locales.map((locale) => ({ locale }));
}

export default async function RootLayout({
  children,
  params: { locale },
}: RootLayoutProps) {
  return (
    <html lang={locale}>
      <head>
        <meta name='application-name' content='DjangoAsyncZip' />
        <meta name='apple-mobile-web-app-capable' content='yes' />
        <meta name='apple-mobile-web-app-status-bar-style' content='default' />
        <meta name='apple-mobile-web-app-title' content='DjangoAsyncZip' />
        <meta name='description' content='' />
        <meta name='format-detection' content='telephone=no' />
        <meta name='mobile-web-app-capable' content='yes' />
        <meta name='msapplication-tap-highlight' content='no' />
        <meta name='theme-color' content='#000000' />
      </head>
      <body>{children}</body>
    </html>
  );
}
