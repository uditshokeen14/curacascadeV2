"""Generate vector diagrams for schema architecture and taxonomy tree."""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 9.5,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

def generate_figure_schema():
    fig, ax = plt.subplots(figsize=(12, 6.0))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    ax.axis("off")

    # Schema boxes
    tables = [
        {"x": 0.05, "y": 0.58, "w": 0.26, "h": 0.36, "title": "GENES (Core Entity)",
         "fields": [
             ("PK", "gene_symbol (TEXT)"),
             ("ATTR", "hgnc_id (TEXT)"),
             ("ATTR", "entrez_id (TEXT)"),
             ("ATTR", "chromosome (TEXT)"),
             ("FLAG", "is_downgraded (INT)"),
             ("FLAG", "highest_severity (TEXT)")
         ], "header_color": "#0284c7"},
        {"x": 0.69, "y": 0.58, "w": 0.26, "h": 0.36, "title": "DISEASES (Ontology)",
         "fields": [
             ("PK", "disease_id (TEXT)"),
             ("ATTR", "disease_name (TEXT)"),
             ("ATTR", "mondo_id (TEXT)"),
             ("ATTR", "omim_id (TEXT)"),
             ("ATTR", "inheritance_mode (TEXT)"),
             ("STAT", "prevalence_per_million (REAL)")
         ], "header_color": "#0d9488"},
        {"x": 0.05, "y": 0.08, "w": 0.26, "h": 0.38, "title": "CLINGEN_CURATIONS (Upstream)",
         "fields": [
             ("PK", "curation_id (INTEGER)"),
             ("FK", "gene_symbol -> genes"),
             ("FK", "disease_id -> diseases"),
             ("KEY", "classification (TEXT)"),
             ("DATE", "classification_date (TEXT)"),
             ("META", "gcep (TEXT) | moi (TEXT)")
         ], "header_color": "#6366f1"},
        {"x": 0.37, "y": 0.08, "w": 0.26, "h": 0.38, "title": "CLINVAR_VARIANTS (Downstream)",
         "fields": [
             ("PK", "variation_id (INTEGER)"),
             ("FK", "gene_symbol -> genes"),
             ("FK", "disease_id -> diseases"),
             ("KEY", "is_plp (INT) | clinical_sig"),
             ("CONF", "stars (0-4) | submitters (INT)"),
             ("POP", "gnomad_af_global / popmax")
         ], "header_color": "#f59e0b"},
        {"x": 0.69, "y": 0.08, "w": 0.26, "h": 0.38, "title": "PANELAPP_ENTRIES (Downstream)",
         "fields": [
             ("PK", "entry_id (INTEGER)"),
             ("FK", "gene_symbol -> genes"),
             ("FK", "disease_id -> diseases"),
             ("KEY", "confidence ('green'/'amber')"),
             ("META", "panel_id (INT) | panel_name"),
             ("DATE", "saved_date (TEXT)")
         ], "header_color": "#10b981"},
        {"x": 0.37, "y": 0.60, "w": 0.26, "h": 0.34, "title": "AUDIT_FINDINGS (Materialized)",
         "fields": [
             ("PK", "finding_id (INTEGER)"),
             ("CLASS", "audit_class ('A'|'B'|'C')"),
             ("SEV", "severity ('CRITICAL'|'HIGH')"),
             ("LAT", "days_unresolved (INTEGER)"),
             ("MCAF", "gnomad_af | mcaf_ceiling")
         ], "header_color": "#dc2626"}
    ]

    for tbl in tables:
        # Outer box
        rect = patches.FancyBboxPatch(
            (tbl["x"], tbl["y"]), tbl["w"], tbl["h"],
            boxstyle="round,pad=0.015,rounding_size=0.025",
            facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.5
        )
        ax.add_patch(rect)
        # Header banner
        header = patches.FancyBboxPatch(
            (tbl["x"], tbl["y"] + tbl["h"] - 0.08), tbl["w"], 0.08,
            boxstyle="round,pad=0.015,rounding_size=0.025",
            facecolor=tbl["header_color"], edgecolor=tbl["header_color"], linewidth=1.0
        )
        ax.add_patch(header)
        ax.text(tbl["x"] + tbl["w"]/2, tbl["y"] + tbl["h"] - 0.042, tbl["title"],
                ha="center", va="center", color="white", fontsize=8.8, fontweight="bold")
        
        # Field list
        y_text = tbl["y"] + tbl["h"] - 0.12
        for tag, fld in tbl["fields"]:
            ax.text(tbl["x"] + 0.02, y_text, f"[{tag}]", color="#64748b", fontsize=7.5, fontweight="bold")
            ax.text(tbl["x"] + 0.07, y_text, fld, color="#1e293b", fontsize=7.8)
            y_text -= 0.045

    # Relationship connectors
    # Genes (0.18, 0.58) -> Clingen (0.18, 0.46)
    ax.annotate("", xy=(0.18, 0.47), xytext=(0.18, 0.58), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0284c7"))
    ax.text(0.19, 0.52, "1 : N", fontsize=7.5, fontweight="bold", color="#0284c7")

    # Genes -> ClinVar
    ax.annotate("", xy=(0.42, 0.47), xytext=(0.28, 0.58), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0284c7"))
    ax.text(0.33, 0.53, "1 : N", fontsize=7.5, fontweight="bold", color="#0284c7")

    # Genes -> PanelApp
    ax.annotate("", xy=(0.74, 0.47), xytext=(0.31, 0.70), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0284c7", connectionstyle="arc3,rad=-0.15"))
    
    # Diseases (0.75, 0.58) -> Clingen, ClinVar, PanelApp
    ax.annotate("", xy=(0.82, 0.47), xytext=(0.82, 0.58), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0d9488"))
    ax.text(0.83, 0.52, "1 : N", fontsize=7.5, fontweight="bold", color="#0d9488")
    ax.annotate("", xy=(0.58, 0.47), xytext=(0.73, 0.58), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0d9488"))

    # Audit Findings materialization
    ax.annotate("", xy=(0.50, 0.60), xytext=(0.50, 0.47), arrowprops=dict(arrowstyle="->", lw=2.0, color="#dc2626", linestyle="--"))
    ax.text(0.50, 0.53, "Materialized Cross-Layer Join", ha="center", fontsize=7.8, fontweight="bold", color="#dc2626", backgroundcolor="#ffffff")

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.tight_layout()
    out_path = FIG_DIR / "figure_schema_architecture.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")

def generate_figure_taxonomy():
    fig, ax = plt.subplots(figsize=(11, 4.8))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    ax.axis("off")

    # Tree nodes
    # Root
    root = patches.FancyBboxPatch((0.36, 0.78), 0.28, 0.16, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="#f1f5f9", edgecolor="#475569", lw=1.8)
    ax.add_patch(root)
    ax.text(0.50, 0.88, "ClinGen Upstream Curation", ha="center", va="center", fontweight="bold", fontsize=9.2, color="#0f172a")
    ax.text(0.50, 0.82, "Gene Validity Status?", ha="center", va="center", fontsize=8.2, color="#475569")

    # Branch Left: Disputed or Refuted
    ax.annotate("", xy=(0.28, 0.62), xytext=(0.42, 0.77), arrowprops=dict(arrowstyle="->", lw=2.0, color="#dc2626"))
    ax.text(0.30, 0.71, "Disputed / Refuted", ha="right", fontsize=8.2, fontweight="bold", color="#dc2626")

    # Branch Right: Limited
    ax.annotate("", xy=(0.72, 0.62), xytext=(0.58, 0.77), arrowprops=dict(arrowstyle="->", lw=2.0, color="#d97706"))
    ax.text(0.70, 0.71, "Limited Evidence", ha="left", fontsize=8.2, fontweight="bold", color="#d97706")

    # Middle question for Disputed/Refuted: Downstream Layer?
    mid_node = patches.FancyBboxPatch((0.14, 0.44), 0.28, 0.16, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="#fee2e2", edgecolor="#ef4444", lw=1.6)
    ax.add_patch(mid_node)
    ax.text(0.28, 0.54, "Target Downstream Layer?", ha="center", va="center", fontweight="bold", fontsize=9.0, color="#991b1b")
    ax.text(0.28, 0.48, "ClinVar vs PanelApp", ha="center", va="center", fontsize=8.0, color="#7f1d1d")

    # Leaf 1: Class A
    ax.annotate("", xy=(0.14, 0.26), xytext=(0.22, 0.43), arrowprops=dict(arrowstyle="->", lw=2.0, color="#b91c1c"))
    leaf_a = patches.FancyBboxPatch((0.02, 0.06), 0.26, 0.20, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="#fef2f2", edgecolor="#b91c1c", lw=2.0)
    ax.add_patch(leaf_a)
    ax.text(0.15, 0.21, "CLASS A: CRITICAL", ha="center", va="center", fontweight="bold", fontsize=8.8, color="#991b1b")
    ax.text(0.15, 0.13, "ClinVar P/LP in Refuted Gene\n(Direct False-Positive Risk;\nACMG Guidelines Violated)", ha="center", va="center", fontsize=7.5, color="#450a0a")

    # Leaf 2: Class C
    ax.annotate("", xy=(0.38, 0.26), xytext=(0.34, 0.43), arrowprops=dict(arrowstyle="->", lw=2.0, color="#b91c1c"))
    leaf_c = patches.FancyBboxPatch((0.31, 0.06), 0.26, 0.20, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="#fef2f2", edgecolor="#b91c1c", lw=2.0)
    ax.add_patch(leaf_c)
    ax.text(0.44, 0.21, "CLASS C: CRITICAL", ha="center", va="center", fontweight="bold", fontsize=8.8, color="#991b1b")
    ax.text(0.44, 0.13, "PanelApp 'Green' Diagnostic Tier\nin Refuted Gene\n(Routine Laboratory Screening)", ha="center", va="center", fontsize=7.5, color="#450a0a")

    # Leaf 3: Class B
    leaf_b = patches.FancyBboxPatch((0.65, 0.26), 0.30, 0.34, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="#fffbeb", edgecolor="#d97706", lw=2.0)
    ax.add_patch(leaf_b)
    ax.text(0.80, 0.52, "CLASS B: HIGH SEVERITY", ha="center", va="center", fontweight="bold", fontsize=8.8, color="#92400e")
    ax.text(0.80, 0.39, "ClinVar P/LP in Limited Gene\n\n• ACMG ceiling: Max VUS\n• Premature clinical closure\n• Incomplete evidence base", ha="center", va="center", fontsize=7.8, color="#78350f")

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.tight_layout()
    out_path = FIG_DIR / "figure_taxonomy_tree.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    generate_figure_schema()
    generate_figure_taxonomy()
    print("Schema and taxonomy figures generated!")
