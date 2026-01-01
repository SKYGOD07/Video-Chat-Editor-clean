import { pgTable, text, serial, timestamp, varchar, boolean } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const videos = pgTable("videos", {
  id: serial("id").primaryKey(),
  originalName: text("original_name").notNull(),
  filename: text("filename").notNull(),
  processedFilename: text("processed_filename"),
  status: text("status").notNull().default("uploaded"), // uploaded, processing, completed, error
  progress: text("progress"), // readable status message
  createdAt: timestamp("created_at").defaultNow(),
});

export const insertVideoSchema = createInsertSchema(videos).omit({
  id: true,
  createdAt: true,
  processedFilename: true,
  status: true,
  progress: true
});

export type Video = typeof videos.$inferSelect;
export type InsertVideo = z.infer<typeof insertVideoSchema>;

export const processVideoSchema = z.object({
  command: z.string().min(1)
});

export type ProcessVideoRequest = z.infer<typeof processVideoSchema>;
