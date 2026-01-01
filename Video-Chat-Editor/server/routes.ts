import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";
import { z } from "zod";
import multer from "multer";
import path from "path";
import fs from "fs";
import { spawn } from "child_process";
import express from "express";

const upload = multer({
  storage: multer.diskStorage({
    destination: "uploads/",
    filename: (req, file, cb) => {
      const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
      cb(null, uniqueSuffix + path.extname(file.originalname));
    }
  })
});

// Ensure directories exist
if (!fs.existsSync("uploads")) fs.mkdirSync("uploads");
if (!fs.existsSync("processed")) fs.mkdirSync("processed");

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  
  // Serve static files
  app.use("/uploads", express.static("uploads"));
  app.use("/processed", express.static("processed"));

  // API Routes
  app.get(api.videos.list.path, async (req, res) => {
    const videos = await storage.getVideos();
    res.json(videos);
  });

  app.get(api.videos.get.path, async (req, res) => {
    const video = await storage.getVideo(Number(req.params.id));
    if (!video) return res.status(404).json({ message: "Video not found" });
    res.json(video);
  });

  app.post("/api/videos/upload", upload.single("video"), async (req, res) => {
    if (!req.file) return res.status(400).json({ message: "No file uploaded" });

    const video = await storage.createVideo({
      originalName: req.file.originalname,
      filename: req.file.filename,
      status: "uploaded",
      progress: "Ready to process"
    });

    res.status(201).json(video);
  });

  app.post(api.videos.process.path, async (req, res) => {
    const id = Number(req.params.id);
    const video = await storage.getVideo(id);
    if (!video) return res.status(404).json({ message: "Video not found" });

    try {
      const input = api.videos.process.input.parse(req.body);
      
      // Update status
      await storage.updateVideo(id, { status: "processing", progress: "Starting processing..." });

      // Spawn Python process
      const pythonProcess = spawn("python3", [
        "server/py/processor.py",
        String(id),
        video.filename,
        input.command
      ]);

      pythonProcess.stdout.on("data", async (data) => {
        const lines = data.toString().split("\n");
        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const update = JSON.parse(line);
            console.log("Python update:", update);
            if (update.status || update.progress || update.processedFilename) {
              await storage.updateVideo(id, update);
            }
          } catch (e) {
            console.log("Python stdout (not JSON):", line);
          }
        }
      });

      pythonProcess.stderr.on("data", (data) => {
        console.error("Python stderr:", data.toString());
      });

      pythonProcess.on("close", async (code) => {
        console.log(`Python process exited with code ${code}`);
        if (code !== 0) {
          await storage.updateVideo(id, { status: "error", progress: "Processing failed" });
        }
      });

      res.json({ message: "Processing started", status: "processing" });

    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({ message: err.errors[0].message });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  return httpServer;
}
