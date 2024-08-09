import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  return [
    {
      url: 'https://django-async-zip.com',
      lastModified: new Date(),
    },
  ];
}
