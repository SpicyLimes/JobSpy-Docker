import gradio as gr

# ──────────────────────────────────────────────────────────────────────
# Dark Neon — Gradio Theme
# Dark modern UI with neon blue accents and glow effects
# ──────────────────────────────────────────────────────────────────────

# Neon blue color scale
neon_blue = gr.themes.Color(
    c50="#e6fbff",  c100="#b3f3ff",  c200="#66e8ff",
    c300="#00daff",  c400="#00c8ff",  c500="#00aed8",
    c600="#0094b8",  c700="#007898",  c800="#005a72",
    c900="#003d50",  c950="#001e28",
)

# Deep navy neutral scale
deep_navy = gr.themes.Color(
    c50="#e8edf5",  c100="#c5d0e2",  c200="#9aafc8",
    c300="#7090b0",  c400="#506e8c",  c500="#354f68",
    c600="#1e3348",  c700="#111f30",  c800="#0b1422",
    c900="#060c16",  c950="#03060b",
)

theme = gr.themes.Base(
    primary_hue=neon_blue,
    secondary_hue=neon_blue,
    neutral_hue=deep_navy,
    font=[gr.themes.GoogleFont("Space Grotesk"), "ui-sans-serif", "system-ui"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace"],
).set(
    # ── Background ───────────────────────────────────────────────────
    body_background_fill              = "#06090f",
    background_fill_primary           = "#0b0f1a",
    background_fill_secondary         = "#0f1525",

    # ── Borders ──────────────────────────────────────────────────────
    border_color_primary              = "#1e2d42",
    border_color_accent               = "#00c8ff",

    # ── Blocks ───────────────────────────────────────────────────────
    block_background_fill             = "#0b0f1a",
    block_border_color                = "#1e2d42",
    block_border_width                = "1px",
    block_label_background_fill       = "#0f1525",
    block_label_text_color            = "#7a8da8",
    block_title_text_color            = "#e4eaf8",
    block_shadow   = "0 0 20px rgba(0,200,255,0.05), 0 4px 8px rgba(0,0,0,0.5)",
    block_radius                      = "12px",

    # ── Inputs ───────────────────────────────────────────────────────
    input_background_fill             = "#0f1525",
    input_border_color                = "#1e2d42",
    input_border_color_focus          = "#00c8ff",
    input_shadow_focus = "0 0 0 2px rgba(0,200,255,0.18), 0 0 12px rgba(0,200,255,0.3)",
    input_radius                      = "8px",

    # ── Primary Button ───────────────────────────────────────────────
    button_primary_background_fill       = "linear-gradient(135deg,#002a3a,#004d6b)",
    button_primary_background_fill_hover = "linear-gradient(135deg,#003a50,#006890)",
    button_primary_border_color          = "#00c8ff",
    button_primary_text_color            = "#00c8ff",
    button_primary_shadow      = "0 0 12px rgba(0,200,255,0.45),0 0 32px rgba(0,200,255,0.18)",
    button_primary_shadow_hover= "0 0 22px rgba(0,200,255,0.65),0 0 64px rgba(0,200,255,0.22)",

    # ── Secondary Button ─────────────────────────────────────────────
    button_secondary_background_fill  = "#0f1525",
    button_secondary_border_color     = "#1e2d42",
    button_secondary_text_color       = "#7a8da8",
    button_secondary_shadow           = "none",

    # ── Accent / Slider ──────────────────────────────────────────────
    slider_color                      = "#00c8ff",
    color_accent                      = "#00c8ff",
    color_accent_soft                 = "rgba(0,200,255,0.12)",

    # ── Text ─────────────────────────────────────────────────────────
    body_text_color                   = "#e4eaf8",
    body_text_color_subdued           = "#7a8da8",

    # ── Code ─────────────────────────────────────────────────────────
    code_background_fill              = "#040608",

    # ── Checkbox ─────────────────────────────────────────────────────
    checkbox_background_color         = "#0f1525",
    checkbox_border_color             = "#1e2d42",
    checkbox_border_color_focus       = "#00c8ff",
    checkbox_border_color_selected    = "#00c8ff",
    checkbox_background_color_selected= "rgba(0,200,255,0.15)",
    checkbox_shadow        = "0 0 6px rgba(0,200,255,0.45)",

    # ── Table ────────────────────────────────────────────────────────
    table_border_color                = "#1e2d42",
    table_even_background_fill        = "#0f1525",
    table_odd_background_fill         = "#0b0f1a",

    # ── Error ────────────────────────────────────────────────────────
    error_background_fill             = "#1a0810",
    error_border_color                = "#ff3366",
    error_text_color                  = "#ff3366",
)

