export class ApiError extends Error {
  constructor(status, requestId) {
    super(`A API retornou HTTP ${status}.`);
    this.name = "ApiError";
    this.status = status;
    this.requestId = requestId;
  }
}

export function createApiClient(baseUrl, fetcher = globalThis.fetch) {
  return {
    async health({ signal } = {}) {
      const response = await fetcher(new URL("/health", baseUrl), { signal });
      if (!response.ok) {
        throw new ApiError(
          response.status,
          response.headers.get("X-Request-ID"),
        );
      }
      const data = await response.json();
      if (data?.status !== "ok") {
        throw new TypeError("Resposta de saúde inválida.");
      }
      return { status: data.status };
    },
  };
}
