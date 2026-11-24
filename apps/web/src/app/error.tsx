"use client";

import { Button } from "@/components/ui/button";

export default function ErrorPage({
  unstable_retry,
}: {
  unstable_retry: () => void;
}) {
  return (
    <section role="alert" className="mx-auto max-w-6xl px-6 py-20">
      <h1 className="mb-6 text-4xl font-bold">
        Não foi possível carregar esta página
      </h1>
      <Button onClick={unstable_retry}>Tentar novamente</Button>
    </section>
  );
}
