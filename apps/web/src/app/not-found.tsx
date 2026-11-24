import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";

export default function NotFound() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20">
      <h1 className="mb-6 text-4xl font-bold">Página não encontrada</h1>
      <Link href="/" className={buttonVariants()}>
        Voltar ao início
      </Link>
    </section>
  );
}
