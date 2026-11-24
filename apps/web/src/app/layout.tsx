import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Loung Work · Loung Tech",
  description: "Plataforma de carreira e busca de vagas da Loung Tech.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body className="flex min-h-dvh flex-col">
        <a
          href="#conteudo"
          className="sr-only focus:not-sr-only focus:absolute focus:z-10 focus:bg-black focus:p-4"
        >
          Pular para o conteúdo
        </a>
        <header className="border-b border-white/15">
          <nav
            aria-label="Principal"
            className="mx-auto flex min-h-18 max-w-6xl flex-wrap items-center justify-between gap-3 px-6 py-3"
          >
            <Link
              href="/"
              className="inline-flex min-h-11 items-center text-xl font-bold tracking-tight"
            >
              Loung<span className="ml-1.5 text-primary">Work</span>
            </Link>
            <Link
              href="/#produto"
              className="inline-flex min-h-11 items-center px-2 text-sm text-white/80 hover:text-primary"
            >
              Sobre o produto
            </Link>
          </nav>
        </header>
        <main id="conteudo" tabIndex={-1} className="flex-1">
          {children}
        </main>
        <footer className="border-t border-white/15">
          <div className="mx-auto max-w-6xl px-6 py-7 text-sm text-white/70">
            Um produto da Loung Tech
          </div>
        </footer>
      </body>
    </html>
  );
}
