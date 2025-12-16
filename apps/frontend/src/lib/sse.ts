export interface SSEOptions {
  url: string;
  headers?: HeadersInit;
}

/**
 * Creates an async iterable from an SSE stream
 * Compatible with React Query's experimental_streamedQuery
 */
export async function* createSSEStream<T>(
  options: SSEOptions
): AsyncGenerator<T> {
  const response = await fetch(options.url, {
    headers: {
      Accept: "text/event-stream",
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(
      `SSE request failed: ${response.status} ${response.statusText}`
    );
  }

  if (!response.body) {
    throw new Error("Response body is null");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      // Decode chunk and add to buffer
      buffer += decoder.decode(value, { stream: true });

      // Split by double newline (SSE message separator)
      const messages = buffer.split("\n\n");

      // Keep last incomplete message in buffer
      buffer = messages.pop() || "";

      // Process complete messages
      for (const message of messages) {
        if (message.startsWith("data: ")) {
          const data = message.slice(6); // Remove "data: " prefix
          try {
            yield JSON.parse(data) as T;
          } catch (e) {
            console.error("Failed to parse SSE message:", data, e);
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}
