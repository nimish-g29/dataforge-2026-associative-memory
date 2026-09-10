from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, KeepTogether)
from reportlab.lib.enums import TA_LEFT

INK = colors.HexColor("#1B1F27")
DIM = colors.HexColor("#5B6270")
AMBER = colors.HexColor("#B4791F")
LINE = colors.HexColor("#D8D5CC")

styles = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15,
                             leading=18, textColor=INK, spaceAfter=2),
    "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=8.7,
                                leading=11, textColor=DIM, spaceAfter=9),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=9.6,
                          leading=11.5, textColor=AMBER, spaceBefore=5.5, spaceAfter=2),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=8.7,
                            leading=11.3, textColor=INK, alignment=TA_LEFT,
                            spaceAfter=3.5),
    "small": ParagraphStyle("small", fontName="Helvetica-Oblique", fontSize=7.6,
                             leading=10, textColor=DIM, spaceAfter=3),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=7.4,
                            leading=9.2, textColor=INK),
    "cellhead": ParagraphStyle("cellhead", fontName="Helvetica-Bold", fontSize=7.6,
                                leading=9.4, textColor=colors.white),
}

doc = SimpleDocTemplate("summary.pdf", pagesize=letter,
                         topMargin=0.45*inch, bottomMargin=0.4*inch,
                         leftMargin=0.6*inch, rightMargin=0.6*inch)

S = []
P = Paragraph

S.append(P("Associative Memory and Synaptic Plasticity: Why Fixed-Size Memory Forgets Gracefully", styles["title"]))
S.append(P("One-page concept summary &nbsp;·&nbsp; DataForge 2026, Pathway track &nbsp;·&nbsp; Concept: Associative Memory / Fast Weights, combined with Synaptic Plasticity as Short-Term Memory", styles["subtitle"]))

S.append(P("The problem and the mechanism", styles["h2"]))
S.append(P(
    "A standard Transformer keeps every past token in a growing key-value cache and compares the "
    "current query against all of them, so cost and memory scale with context length. Associative "
    "memory offers a different contract: information is superposed into a single fixed-size weight "
    "structure through a Hebbian correlation write, M &larr; M + key&otimes;value, and recovered by a "
    "single matched read, value_est = sign(M<super>T</super>&middot;key). This is not a new idea &mdash; "
    "linear correlation-matrix memories (Anderson, Kohonen) and Hopfield networks date to the 1970s&ndash;80s "
    "&mdash; but it has resurfaced as a serious architectural primitive because it gives O(1) memory growth "
    "and constant-time read/write, independent of sequence length. The trade-off is interference: as more "
    "associations share the same synapses, retrieval degrades smoothly rather than failing outright, with "
    "capacity bounded by vector dimensionality rather than by an allocated slot count.", styles["body"]))

S.append(P("Representative systems", styles["h2"]))
S.append(P(
    "Three systems make the landscape concrete. Classical correlation-matrix / Hopfield memory writes "
    "densely and offline, with a hard capacity bound (~0.14N patterns for N-unit Hopfield nets) and no "
    "locality constraint. Fast-weight programmers and modern linear-attention Transformers apply the same "
    "outer-product write incrementally at every token, letting a Transformer-like model compress context "
    "into a fixed-size running state instead of an ever-growing cache. Pathway's Dragon Hatchling (BDH) "
    "instantiates the mechanism as sparse, local Hebbian synapse updates over a scale-free graph of neuron "
    "particles: attention is reported to emerge from these local co-activation writes rather than a dense "
    "global comparison, and BDH additionally offers a GPU-friendly dual formulation (BDH-GPU) that follows "
    "Transformer-like scaling laws.", styles["body"]))

table_data = [
    [P("System", styles["cellhead"]), P("Write rule", styles["cellhead"]),
     P("Structure", styles["cellhead"]), P("Capacity behavior", styles["cellhead"]),
     P("Evidence level", styles["cellhead"])],
    [P("Hopfield / correlation memory", styles["cell"]), P("Dense outer-product, offline", styles["cell"]),
     P("Fully connected", styles["cell"]), P("Hard bound (~0.14N), abrupt collapse above it", styles["cell"]),
     P("Established theory (1970s&ndash;80s)", styles["cell"])],
    [P("Fast weights / linear attention", styles["cell"]), P("Incremental outer-product per token", styles["cell"]),
     P("Dense, sequential", styles["cell"]), P("Graceful degradation, dimension-bounded", styles["cell"]),
     P("Widely reproduced in LLM literature", styles["cell"])],
    [P("BDH Hebbian synapses", styles["cell"]), P("Local, sparse co-activation write", styles["cell"]),
     P("Scale-free particle graph", styles["cell"]), P("Not independently quantified publicly", styles["cell"]),
     P("Developer-reported (Pathway, arXiv 2509.26507)", styles["cell"])],
]
t = Table(table_data, colWidths=[1.05*inch, 1.35*inch, 0.95*inch, 1.5*inch, 1.45*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), INK),
    ("GRID", (0,0), (-1,-1), 0.5, LINE),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 2.5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2.5),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F3F1EA")]),
]))
S.append(t)
S.append(Spacer(1, 6))

S.append(P("Where the concept wins, and where it doesn't", styles["h2"]))
S.append(P(
    "The advantage is structural: constant-size state means no growing cache and no quadratic comparison, "
    "which matters as context and continual-adaptation demands grow. The disadvantage is that dense "
    "correlation memories don't scale directly to LLM-length sequences &mdash; capacity is tied to "
    "dimensionality, so naive superposition saturates quickly. Fast-weight/linear-attention formulations "
    "and BDH's sparsity/locality are both, in different ways, responses to that saturation problem rather "
    "than a way around it. BDH-CQ, a later system built on the same substrate, shows a further consequence: "
    "because demonstrations at inference time simply write into recurrent contextual memory rather than "
    "updating model parameters, a 150M-parameter model can acquire an unseen visual transformation from a "
    "handful of examples with no gradient update. On the public ARC-AGI-1 evaluation set it reached 29.5% "
    "pass@2 at a computed cost of ~$0.0007/task &mdash; a developer-reported result that was independently "
    "re-tested by a team from Bielik AI and NYU, who confirmed it (arXiv 2608.09888). This is an "
    "independent reproduction, not a deployment or a benchmark claim taken at face value. BDH's separately "
    "reported 97.4% accuracy on an extreme-Sudoku benchmark is explicitly attributed by Pathway to an "
    "internal implementation, not the public open-source repository &mdash; a distinction worth preserving "
    "rather than collapsing into one headline number.", styles["body"]))

S.append(P("BDH and BDH-CQ, specifically", styles["h2"]))
S.append(P(
    "BDH's role is architectural: its attention mechanism is a literal instance of the Hebbian "
    "outer-product write described above, applied locally and sparsely across a particle graph rather than "
    "as one dense matrix. BDH-CQ's role is functional: it demonstrates what that mechanism buys at "
    "inference time &mdash; task adaptation through memory writes instead of weight updates. The two are "
    "not redundant citations; BDH explains the mechanism, BDH-CQ evidences one consequence of it.", styles["body"]))

S.append(P("Open limitation", styles["h2"]))
S.append(P(
    "The clearest unresolved question, raised in public review of the BDH-CQ paper itself, is whether "
    "demonstration ingestion is forward-only conditioning of recurrent state or involves some form of "
    "online parameter adjustment &mdash; the paper's own language (\"modifies recurrent memory\") does not "
    "fully disambiguate this, and it matters for how strongly the continual-learning framing can be taken. "
    "Separately, BDH-CQ's controlled evaluations report weaknesses on ordering, nesting, conditional rule "
    "selection, and compositional generalization &mdash; the interference this explainer makes tangible at "
    "toy scale has a direct analogue in these model-scale failure modes.", styles["body"]))

S.append(P(
    "Primary sources: Pathway, \"The Dragon Hatchling: The Missing Link between the Transformer and Models "
    "of the Brain,\" arXiv:2509.26507. Pathway, \"BDH-CQ: In-Context Learning with Recurrent Latent "
    "Reasoning,\" arXiv:2608.09888. Pathway BDH GitHub repository (pathwaycom/bdh) for the Sudoku-benchmark "
    "scope caveat. Classical associative memory: J.A. Anderson (1972) and T. Kohonen (1972) on "
    "correlation-matrix memories; J.J. Hopfield (1982) on associative neural networks.", styles["small"]))

doc.build(S)
print("done")
