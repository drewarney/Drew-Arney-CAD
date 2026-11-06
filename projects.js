// ─────────────────────────────────────────────────────────────
//  Your portfolio content lives here.
//  To add a project: copy one { ... } block, change the fields,
//  drop the STL into /models and the sheet PNGs/PDF into /drawings.
// ─────────────────────────────────────────────────────────────

export const SITE = {
  name: "Drew Arney CAD",
  short: "DAC",
  tagline: "Sketches, samples, and old prints turned into clean 3D models and machinist-ready drawings for machine shops and hardware teams across the country.",
  location: "San Luis Obispo, CA",
  email: "drew@drewarneycad.com",
  phone: "(925) 330-4207",    // ← leave "" to hide it
  hours: "Mon–Sat",
};

// Gallery is empty for now. When a project is cleared to show, add it like this:
//
//  {
//    title: "Part Name",
//    dwg: "1234", date: "Jan 2027", material: "6061-T6 Aluminum", standard: "ASME Y14.5-2018",
//    summary: "One or two sentences about the part.",
//    highlights: ["Key feature", "Key tolerance"],
//    model: ["models/part-1.stl"],          // STL file(s) in /models
//    pdf: "drawings/part.pdf",              // optional
//    sheets: [{ src: "drawings/part-sheet-1.png", label: "Sheet 1" }],
//  },
export const PROJECTS = [];

export const SERVICES = [
  {
    title: "3D Modeling",
    body: "Parts and assemblies built in Fusion (or your CAD system) from sketches, old prints, or a physical sample you send over.",
  },
  {
    title: "Production Drawings",
    body: "Machinist-ready drawings with front, top, and side views, a sensible datum scheme, and GD&T per ASME Y14.5.",
  },
  {
    title: "Drawing Cleanup & Redraws",
    body: "Legacy or hand-drawn prints converted into modern CAD with consistent title blocks and revision control.",
  },
  {
    title: "DFM Review",
    body: "Customer models checked before you quote: deep pockets with sharp internal corners that need tiny end mills, unmachinable blind holes, and tolerances tighter than the part needs.",
  },
  {
    title: "CAM-Ready Model Cleanup",
    body: "Cosmetic chamfers, fillets, and minor features that get in the way of fixturing or toolpaths removed, so your machinists can program faster.",
  },
  {
    title: "Fixture & Workholding Design",
    body: "Send the part geometry and your vise or table specs, and get custom soft jaws, modular fixture plates, or welding jigs modeled and ready to cut on the shop floor.",
  },
  {
    title: "Inspection & FAIR Documentation",
    body: "Ballooned drawings with numbered callouts, plus QC measurement logs tied to each GD&T callout, in Excel or PDF, for First Article Inspection Reports.",
  },
  {
    title: "Reverse Engineering from Measurements",
    body: "Send caliper, micrometer, or height-gauge readings with photos and sketches, and get back a fully constrained 3D model and a 2D print.",
  },
];
