import { z } from "zod";
import { videos, insertVideoSchema, processVideoSchema } from "./schema";

export const api = {
  videos: {
    list: {
      method: "GET" as const,
      path: "/api/videos",
      responses: {
        200: z.array(z.custom<typeof videos.$inferSelect>())
      }
    },
    get: {
      method: "GET" as const,
      path: "/api/videos/:id",
      responses: {
        200: z.custom<typeof videos.$inferSelect>(),
        404: z.object({ message: z.string() })
      }
    },
    process: {
      method: "POST" as const,
      path: "/api/videos/:id/process",
      input: processVideoSchema,
      responses: {
        200: z.object({ message: z.string(), status: z.string() }),
        404: z.object({ message: z.string() }),
        400: z.object({ message: z.string() })
      }
    },
    download: {
      method: "GET" as const,
      path: "/api/videos/:id/download",
      responses: {
        200: z.any(), // Stream/File
        404: z.object({ message: z.string() })
      }
    }
  }
};

export function buildUrl(path: string, params?: Record<string, string | number>): string {
  let url = path;
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (url.includes(`:${key}`)) {
        url = url.replace(`:${key}`, String(value));
      }
    });
  }
  return url;
}
