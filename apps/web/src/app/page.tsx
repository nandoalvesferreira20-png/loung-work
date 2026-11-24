import { buttonVariants } from "@/components/ui/button";

const capabilities = [
  [
    "Busca de vagas",
    "Encontre oportunidades por cargo, localidade e modalidade e siga para o site de candidatura.",
  ],
  [
    "Currículo",
    "Organize sua trajetória em um currículo que sistemas de triagem de candidaturas (ATS) consigam ler.",
  ],
  [
    "Análise com IA",
    "Compare seu currículo aos requisitos de uma vaga e identifique pontos fortes e lacunas.",
  ],
];

export default function Home() {
  return (
    <>
      <section className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <p className="mb-5 font-medium text-primary">
          Carreira e busca de vagas
        </p>
        <h1 className="max-w-4xl text-5xl leading-[1.02] font-bold tracking-tight sm:text-7xl">
          Encontre vagas que combinam com sua trajetória.
        </h1>
        <p className="mt-6 max-w-xl text-lg leading-relaxed text-white/75">
          O Loung Work é uma plataforma em desenvolvimento para pesquisar vagas,
          preparar seu currículo e acompanhar candidaturas.
        </p>
        <a className={buttonVariants({ className: "mt-8" })} href="#produto">
          Conheça o produto
        </a>
      </section>
      <section
        id="produto"
        aria-labelledby="produto-titulo"
        className="bg-primary text-primary-foreground"
      >
        <div className="mx-auto max-w-6xl px-6 py-14 sm:py-18">
          <h2
            id="produto-titulo"
            className="mb-8 text-3xl font-bold tracking-tight"
          >
            Recursos planejados
          </h2>
          <ul className="grid gap-6 md:grid-cols-3">
            {capabilities.map(([title, description]) => (
              <li key={title} className="border-t border-black/35 pt-4">
                <h3 className="text-xl font-semibold">{title}</h3>
                <p className="mt-2 leading-relaxed">{description}</p>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </>
  );
}
