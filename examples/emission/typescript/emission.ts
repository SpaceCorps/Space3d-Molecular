// spaceemit client example (TypeScript, Node 18+ / Deno / browsers — uses fetch).
//   SPACEEMIT_URL=http://localhost:8741 node emission.ts      (Node 23.6+; or: npx tsx emission.ts)
const URL = (globalThis as any).process?.env?.SPACEEMIT_URL ?? "http://localhost:8741";

type NumOrArray = number | number[];

interface EmissionRequest {
  field: NumOrArray;              // V/nm
  workFunction: NumOrArray;       // eV
  radius?: number | number[] | null; // nm, omit/null = planar
  gamma?: NumOrArray;
  temperature?: NumOrArray;       // K
  effectiveMass?: NumOrArray;     // m_e
  bandDepth?: NumOrArray;         // eV
  options?: { mode?: "exact" | "wkb"; tolerance?: number };
}

interface EmissionResponse {
  count: number;
  currentDensity: (number | null)[];  // A/nm^2
  nottinghamHeat: (number | null)[];  // W/nm^2, negative = emitter heated
  meanEnergy: (number | null)[];      // eV relative to E_F
  barrierTop: (number | null)[];      // eV relative to E_F
  regime: ("field" | "intermediate" | "thermionic" | null)[];
  errors: { index: number; code: string; message: string }[];
  elapsedMs: number;
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(URL + path, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(`${json.error.code}: ${json.error.message}`);
  return json as T;
}

const req: EmissionRequest = { field: [3, 5, 8], radius: 50, workFunction: 4.5, temperature: [300, 1000, 2000] };
const r = await post<EmissionResponse>("/v1/emission", req);
r.currentDensity.forEach((j, i) =>
  console.log(`F=${(req.field as number[])[i]} V/nm  J=${j?.toExponential(3)} A/nm²  P_N=${r.nottinghamHeat[i]?.toExponential(3)} W/nm²  ${r.regime[i]}`),
);
