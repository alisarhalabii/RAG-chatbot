import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RAG Chatbot | Alisar Halabi",
  description:
    "A Retrieval-Augmented Generation chatbot that answers questions grounded in a document knowledge base.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
