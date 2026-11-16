/*
 * Optional Equinox GTK3 frame compatibility module.
 *
 * GTK3 collapses GtkFrame::shadow-type IN, OUT, ETCHED_IN and ETCHED_OUT
 * to the same CSS border node. The original GTK2 Equinox renderer treated
 * them differently. This module supplies the missing CSS classes on all
 * mapped GtkFrame widgets without patching or subclassing GTK.
 *
 * Opt in for a single GTK3 process using GTK3_MODULES. The normal GTK2
 * engine and GTK3-only CSS themes work without this module.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */
#include <gtk/gtk.h>
#include <gmodule.h>

static const char *const frame_classes[] = {
  "eqx-shadow-in",
  "eqx-shadow-out",
  "eqx-shadow-etched-in",
  "eqx-shadow-etched-out"
};

static void
update_frame_classes (GtkFrame *frame)
{
  GtkStyleContext *style = gtk_widget_get_style_context (GTK_WIDGET (frame));
  GtkShadowType shadow = gtk_frame_get_shadow_type (frame);
  const gchar *wanted = NULL;

  switch (shadow) {
  case GTK_SHADOW_IN:         wanted = frame_classes[0]; break;
  case GTK_SHADOW_OUT:        wanted = frame_classes[1]; break;
  case GTK_SHADOW_ETCHED_IN:  wanted = frame_classes[2]; break;
  case GTK_SHADOW_ETCHED_OUT: wanted = frame_classes[3]; break;
  case GTK_SHADOW_NONE:
  default: break;
  }

  for (guint i = 0; i < G_N_ELEMENTS (frame_classes); i++)
    gtk_style_context_remove_class (style, frame_classes[i]);
  if (wanted)
    gtk_style_context_add_class (style, wanted);
}

static void
on_shadow_changed (GObject *object, GParamSpec *pspec, gpointer user_data)
{
  (void) pspec;
  (void) user_data;
  if (GTK_IS_FRAME (object))
    update_frame_classes (GTK_FRAME (object));
}

static gboolean
on_widget_map (GSignalInvocationHint *hint, guint n_values,
               const GValue *values, gpointer user_data)
{
  (void) hint;
  (void) user_data;
  if (n_values < 1 || !G_VALUE_HOLDS_OBJECT (&values[0]))
    return TRUE;

  GObject *object = g_value_get_object (&values[0]);
  if (!object || !GTK_IS_FRAME (object))
    return TRUE;

  GtkFrame *frame = GTK_FRAME (object);
  if (!g_object_get_data (object, "equinox-frame-compat-connected")) {
    g_signal_connect (frame, "notify::shadow-type",
                      G_CALLBACK (on_shadow_changed), NULL);
    g_object_set_data (object, "equinox-frame-compat-connected",
                       GINT_TO_POINTER (1));
  }
  update_frame_classes (frame);
  return TRUE; /* Keep the hook active for subsequently mapped frames. */
}

/* GTK3 plugin entry point, invoked from GTK3_MODULES on gtk_init(). */
G_MODULE_EXPORT void
gtk_module_init (gint *argc, gchar ***argv)
{
  (void) argc;
  (void) argv;

  /* GtkWidget must be initialized for its 'map' signal to exist. */
  gpointer widget_class = g_type_class_ref (GTK_TYPE_WIDGET);
  const guint map_signal = g_signal_lookup ("map", GTK_TYPE_WIDGET);
  if (map_signal != 0)
    g_signal_add_emission_hook (map_signal, 0, on_widget_map, NULL, NULL);
  g_type_class_unref (widget_class);
}
