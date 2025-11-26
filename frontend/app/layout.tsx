import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Entertainment Graph - System Comparison',
  description: 'Compare retrieval systems for entertainment discovery',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
