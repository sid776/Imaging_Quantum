import './styles/globals.css';

export const metadata = {
  title: 'Quantum Medical Image Scanner',
  description: 'An application leveraging quantum computing for medical image analysis',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
} 