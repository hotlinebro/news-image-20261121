// news-image-20261121 entrypoint: copy the rendered front page to /output.
// Node 22, standard library only. Deterministic: byte-for-byte copy, verified.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
// Verify the copy is complete: a truncated output would silently break the entry.
const srcBytes = statSync(src).size;
const dstBytes = statSync(dst).size;
if (srcBytes !== dstBytes) {
  throw new Error(`entry.png copy incomplete: ${dstBytes} of ${srcBytes} bytes`);
}
console.log(`wrote ${dst} (${dstBytes} bytes)`);
