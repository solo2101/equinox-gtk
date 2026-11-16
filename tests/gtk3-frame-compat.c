/*
 * Integration test: GTK3_MODULES assigns actual GtkFrame shadow CSS classes.
 * Run under an X server (xvfb-run works for CI).
 */
#include <gtk/gtk.h>

static const struct {
  GtkShadowType shadow;
  const char *name;
} cases[] = {
  {GTK_SHADOW_IN, "eqx-shadow-in"},
  {GTK_SHADOW_OUT, "eqx-shadow-out"},
  {GTK_SHADOW_ETCHED_IN, "eqx-shadow-etched-in"},
  {GTK_SHADOW_ETCHED_OUT, "eqx-shadow-etched-out"}
};

int
main (int argc, char **argv)
{
  if (!gtk_init_check (&argc, &argv)) {
    g_printerr ("Unable to initialize GTK3 display\n");
    return 2;
  }
  GtkWidget *win = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  GtkWidget *container = gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 8);
  gtk_container_add (GTK_CONTAINER (win), container);
  GtkWidget *frames[G_N_ELEMENTS (cases)];

  for (guint i = 0; i < G_N_ELEMENTS (cases); i++) {
    frames[i] = gtk_frame_new ("Frame shadow test");
    gtk_frame_set_shadow_type (GTK_FRAME (frames[i]), cases[i].shadow);
    gtk_widget_set_size_request (frames[i], 130, 60);
    gtk_box_pack_start (GTK_BOX (container), frames[i], TRUE, TRUE, 0);
  }

  gtk_widget_show_all (win);
  while (gtk_events_pending ())
    gtk_main_iteration ();

  gboolean ok = TRUE;
  for (guint i = 0; i < G_N_ELEMENTS (cases); i++) {
    GtkStyleContext *style = gtk_widget_get_style_context (frames[i]);
    if (!gtk_style_context_has_class (style, cases[i].name)) {
      g_printerr ("Missing compatibility class: %s\n", cases[i].name);
      ok = FALSE;
    }
  }

  gtk_frame_set_shadow_type (GTK_FRAME (frames[0]), GTK_SHADOW_OUT);
  GtkStyleContext *changed = gtk_widget_get_style_context (frames[0]);
  if (!gtk_style_context_has_class (changed, "eqx-shadow-out") ||
      gtk_style_context_has_class (changed, "eqx-shadow-in")) {
    g_printerr ("Dynamic shadow-type changes not reflected in CSS classes\n");
    ok = FALSE;
  }

  gtk_widget_destroy (win);
  if (ok)
    g_print ("PASS: Four GtkFrame shadow classes and dynamic state change\n");
  return ok ? 0 : 1;
}
