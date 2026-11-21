// news-image-20261121 v2 entrypoint.
// Copies entry.png into the output directory and verifies the copy is
// byte-identical to the source. Node 22, standard library only.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);

if (!existsSync(src)) {
  throw new Error("entry.png is missing next to main.ts");
}

const source = readFileSync(src);
if (source.length === 0) {
  throw new Error("entry.png is empty");
}
if (source.subarray(1, 4).toString("ascii") !== "PNG") {
  throw new Error("entry.png does not look like a PNG file");
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);

const copied = readFileSync(dest);
if (!copied.equals(source)) {
  throw new Error("copied entry.png differs from the source");
}
const size = statSync(dest).size;
if (size !== source.length) {
  throw new Error(`size mismatch after copy: ${size} vs ${source.length}`);
}
if (size > 1024 * 1024) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}

console.log(`entry.png copied to ${dest} (${size} bytes, verified byte-identical)`);
