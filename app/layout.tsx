import type { Metadata } from "next";
import { Inter, Rye } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const rye = Rye({ weight: "400", subsets: ["latin"], variable: "--font-rye" });

export const metadata: Metadata = {
  title: "The Remy Digest",
  description: "The premier publication for the discerning dachshund.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${rye.variable} bg-[#FDFBF7]`}>
        {children}
      </body>
    </html>
  );
}