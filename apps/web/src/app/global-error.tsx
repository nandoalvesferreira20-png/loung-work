"use client";

import "./globals.css";
import { Button } from "@/components/ui/button";

export default function GlobalError({
  unstable_retry,
}: {
  unstable_retry: () => void;
}) {
  return (
    <html lang="pt-BR">
      <body>
        <main role="alert" className="mx-auto max-w-6xl px-6 py-20">
          <h1 className="mb-6 text-4xl font-bold">
            Não foi possível carregar o Loung Work
          </h1>
          <Button onClick={unstable_retry}>Tentar novamente</Button>
        </main>
      </body>
    </html>
  );
}
