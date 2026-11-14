import { Config } from "@remotion/cli/config";
import { existsSync } from "node:fs";
// "angle" uses the GPU. On a Linux machine with no GPU (e.g. a cloud container) fall back to software WebGL.
const noGpu = process.platform === "linux" && !existsSync("/dev/dri");
Config.setChromiumOpenGlRenderer(noGpu ? "swangle" : "angle");
Config.setConcurrency(1);
