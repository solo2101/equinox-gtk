/*
 * Equinox GTK3 rendering experiment.
 *
 * Uses the original Equinox 1.50 Cairo drawing routines without changing
 * the GTK2 engine. Build alongside src/equinox_draw.c and src/support.c.
 *
 * No X display or GTK initialization is required. The output is a set of
 * image surfaces for GTK3 border-image styling.
 */
#include <gtk/gtk.h>
#include <cairo.h>
#include <glib/gstdio.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "equinox_draw.h"
#include "support.h"

typedef struct {
    const char *normal_bg, *active_bg, *hover_bg, *selected_bg, *disabled_bg;
    const char *normal_base, *active_base, *hover_base, *disabled_base;
    const char *fg, *disabled_fg;
} Palette;

static const Palette LIGHT = {
    "#d7d7d7", "#bcbcbc", "#e8e8e8", "#3978b4", "#d7d7d7",
    "#ffffff", "#e6e6e6", "#ffffff", "#eeeeee",
    "#252525", "#686868"
};
static const Palette MIDNIGHT = {
    "#4e4e4e", "#3b3b3b", "#6a6a6a", "#497da5", "#4e4e4e",
    "#383838", "#424242", "#404040", "#424242",
    "#dddddd", "#999999"
};

static EquinoxRGB parse_rgb(const char *hex)
{
    unsigned int red = 0, green = 0, blue = 0;
    if (sscanf(hex, "#%02x%02x%02x", &red, &green, &blue) != 3) {
        g_printerr("Invalid color: %s\n", hex);
        exit(1);
    }
    EquinoxRGB c = { red / 255.0, green / 255.0, blue / 255.0 };
    return c;
}

static void init_colors(EquinoxColors *colors, const Palette *p)
{
    static const double shade_factors[] = {
        1.15, 1.04, 0.94, 0.80, 0.70, 0.64, 0.50, 0.45, 0.40
    };
    memset(colors, 0, sizeof(*colors));
    const char *bg[5] = {
        p->normal_bg, p->active_bg, p->hover_bg,
        p->selected_bg, p->disabled_bg
    };
    const char *base[5] = {
        p->normal_base, p->active_base, p->hover_base,
        p->selected_bg, p->disabled_base
    };
    for (int i = 0; i < 5; i++) {
        colors->bg[i] = parse_rgb(bg[i]);
        colors->base[i] = parse_rgb(base[i]);
        colors->fg[i] = parse_rgb(i == GTK_STATE_INSENSITIVE ? p->disabled_fg : p->fg);
        colors->text[i] = colors->fg[i];
    }
    /* Exactly the shade/spot initialization used by equinox_style_realize(). */
    for (int i = 0; i < 9; i++) {
        equinox_shade(&colors->bg[GTK_STATE_NORMAL], &colors->shade[i],
                     (shade_factors[i] - 0.7) * 1.0 + 0.7);
    }
    equinox_shade(&colors->bg[GTK_STATE_SELECTED], &colors->spot[0], 1.42);
    equinox_shade(&colors->bg[GTK_STATE_SELECTED], &colors->spot[1], 1.00);
    equinox_shade(&colors->bg[GTK_STATE_SELECTED], &colors->spot[2], 0.65);
}

static WidgetParameters make_widget(const EquinoxColors *colors,
                                    GtkStateType state, gboolean active,
                                    gboolean focus)
{
    WidgetParameters w;
    memset(&w, 0, sizeof(w));
    w.state_type = (EquinoxStateType)state;
    w.prev_state_type = w.state_type;
    w.active = active;
    w.prelight = (state == GTK_STATE_PRELIGHT);
    w.disabled = (state == GTK_STATE_INSENSITIVE);
    w.focus = focus;
    w.is_default = FALSE;
    w.corners = EQX_CORNER_ALL;
    w.xthickness = 2;
    w.ythickness = 2;
    w.parentbg = colors->bg[GTK_STATE_NORMAL];
    w.curvature = 5.0;
    w.ltr = TRUE;
    w.trans = 1.0;
    return w;
}

static gboolean save_asset(const gchar *dir, const gchar *name,
                           const EquinoxColors *colors, int width, int height,
                           const char *kind, GtkStateType state,
                           gboolean active, gboolean focus,
                           EquinoxGapSide gap_side)
{
    gchar *path = g_build_filename(dir, name, NULL);
    cairo_surface_t *surface = cairo_image_surface_create(
        CAIRO_FORMAT_ARGB32, width, height);
    if (cairo_surface_status(surface) != CAIRO_STATUS_SUCCESS) {
        g_printerr("Cannot allocate %s\n", path);
        g_free(path);
        cairo_surface_destroy(surface);
        return FALSE;
    }
    cairo_t *cr = cairo_create(surface);
    cairo_set_operator(cr, CAIRO_OPERATOR_CLEAR);
    cairo_paint(cr);
    cairo_set_operator(cr, CAIRO_OPERATOR_OVER);
    cairo_set_line_width(cr, 1.0);
    cairo_set_line_cap(cr, CAIRO_LINE_CAP_SQUARE);
    cairo_set_line_join(cr, CAIRO_LINE_JOIN_MITER);

    WidgetParameters w = make_widget(colors, state, active, focus);
    if (!strcmp(kind, "button")) {
        equinox_draw_button(cr, colors, &w, 0, 0, width, height, 0);
    } else if (!strcmp(kind, "entry")) {
        EntryParameters entry;
        memset(&entry, 0, sizeof(entry));
        entry.type = EQX_ENTRY_NORMAL;
        equinox_draw_entry(cr, colors, &w, &entry,
                           0, 0, width, height, 1);
    } else if (!strcmp(kind, "tab")) {
        TabParameters tab;
        memset(&tab, 0, sizeof(tab));
        tab.gap_side = gap_side;
        tab.first_tab = FALSE;
        tab.last_tab = FALSE;
        equinox_draw_tab(cr, colors, &w, &tab,
                         0, 0, width, height);
    } else {
        g_printerr("Unknown asset type: %s\n", kind);
        cairo_destroy(cr);
        cairo_surface_destroy(surface);
        g_free(path);
        return FALSE;
    }
    cairo_status_t draw_status = cairo_status(cr);
    cairo_destroy(cr);
    cairo_status_t png_status = cairo_surface_write_to_png(surface, path);
    cairo_surface_destroy(surface);
    if (draw_status != CAIRO_STATUS_SUCCESS || png_status != CAIRO_STATUS_SUCCESS) {
        g_printerr("Failed drawing %s: %s / %s\n", path,
                   cairo_status_to_string(draw_status),
                   cairo_status_to_string(png_status));
        g_free(path);
        return FALSE;
    }
    g_print("Created %s\n", path);
    g_free(path);
    return TRUE;
}

int main(int argc, char **argv)
{
    if (argc != 3 || (strcmp(argv[1], "light") && strcmp(argv[1], "midnight"))) {
        g_printerr("Usage: %s light|midnight OUTPUT_DIRECTORY\n", argv[0]);
        return 2;
    }
    const Palette *palette = !strcmp(argv[1], "light") ? &LIGHT : &MIDNIGHT;
    if (g_mkdir_with_parents(argv[2], 0755) != 0) {
        g_printerr("Cannot create directory %s\n", argv[2]);
        return 1;
    }
    EquinoxColors colors;
    init_colors(&colors, palette);
    gboolean ok = TRUE;
#define EXPORT(name, w, h, kind, state, active, focus, gap) \
    do { if (!save_asset(argv[2], name, &colors, w, h, kind, \
                         state, active, focus, gap)) ok = FALSE; } while (0)
    EXPORT("button-normal.png", 48, 30, "button", GTK_STATE_NORMAL, FALSE, FALSE, EQX_GAP_BOTTOM);
    EXPORT("button-hover.png", 48, 30, "button", GTK_STATE_PRELIGHT, FALSE, FALSE, EQX_GAP_BOTTOM);
    EXPORT("button-pressed.png", 48, 30, "button", GTK_STATE_ACTIVE, TRUE, FALSE, EQX_GAP_BOTTOM);
    EXPORT("button-disabled.png", 48, 30, "button", GTK_STATE_INSENSITIVE, FALSE, FALSE, EQX_GAP_BOTTOM);
    EXPORT("button-focus.png", 48, 30, "button", GTK_STATE_NORMAL, FALSE, TRUE, EQX_GAP_BOTTOM);
    EXPORT("entry-normal.png", 48, 30, "entry", GTK_STATE_NORMAL, FALSE, FALSE, EQX_GAP_BOTTOM);
    EXPORT("entry-focused.png", 48, 30, "entry", GTK_STATE_NORMAL, FALSE, TRUE, EQX_GAP_BOTTOM);
    EXPORT("entry-disabled.png", 48, 30, "entry", GTK_STATE_INSENSITIVE, FALSE, FALSE, EQX_GAP_BOTTOM);
    /* In the original renderer, GTK_STATE_ACTIVE is the inactive tab. */
    EXPORT("tab-top-selected.png", 56, 28, "tab", GTK_STATE_NORMAL, FALSE, FALSE, EQX_GAP_BOTTOM);
    EXPORT("tab-top-inactive.png", 56, 28, "tab", GTK_STATE_ACTIVE, TRUE, FALSE, EQX_GAP_BOTTOM);
    EXPORT("tab-bottom-selected.png", 56, 28, "tab", GTK_STATE_NORMAL, FALSE, FALSE, EQX_GAP_TOP);
    EXPORT("tab-bottom-inactive.png", 56, 28, "tab", GTK_STATE_ACTIVE, TRUE, FALSE, EQX_GAP_TOP);
    EXPORT("tab-left-selected.png", 28, 56, "tab", GTK_STATE_NORMAL, FALSE, FALSE, EQX_GAP_RIGHT);
    EXPORT("tab-left-inactive.png", 28, 56, "tab", GTK_STATE_ACTIVE, TRUE, FALSE, EQX_GAP_RIGHT);
    EXPORT("tab-right-selected.png", 28, 56, "tab", GTK_STATE_NORMAL, FALSE, FALSE, EQX_GAP_LEFT);
    EXPORT("tab-right-inactive.png", 28, 56, "tab", GTK_STATE_ACTIVE, TRUE, FALSE, EQX_GAP_LEFT);
#undef EXPORT
    return ok ? 0 : 1;
}
