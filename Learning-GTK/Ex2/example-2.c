#include <gtk/gtk.h>

static void print_hello(GtkWidget* widget, gpointer data)
{
    g_print("Hello World\n");
}

static void activate(GtkApplication* app, gpointer user_data)
{
    GtkWidget* window;
    GtkWidget* grid;
    GtkWidget* button;
    
    /* Create a new window and set its title */
    window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "Window");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);

    /* Construct the container that will pack our buttons */
    grid = gtk_grid_new();

    /* Pack the container into the window */
    gtk_container_add(GTK_CONTAINER(window), grid);

    /* Create button 1 with label */
    button = gtk_button_new_with_label("Button 1");
    /* Connect button widget to callback function */
    g_signal_connect(button, "clicked", G_CALLBACK(print_hello), NULL);

    /* Place first button in grid cell (0, 0) 
     * and make it fill 1 cell horizontally and vertically (no spanning)
     */
    gtk_grid_attach(GTK_GRID(grid), button, 0, 0, 1, 1);

    /* Create button 2 with label */
    button = gtk_button_new_with_label("Button 2");
    /* Connect button widget to callback function */
    g_signal_connect(button, "clicked", G_CALLBACK(print_hello), NULL);
    
    /* Place second button in the grid cell (1, 0) 
     * and make it fill just 1 cell horizontall and vertically (no spanning)
     */
    gtk_grid_attach(GTK_GRID(grid), button, 1, 0, 1, 1);
    
    /* Craete quit button with label */
    button = gtk_button_new_with_label("Quit");
    g_signal_connect_swapped(button, "clicked", G_CALLBACK(gtk_widget_destroy), window);

    /* Place Quit button in grid cell (0, 1)
     * and make it span 2 columns.
     */
    gtk_grid_attach(GTK_GRID(grid), button, 0, 1, 2, 1);

    /* Recursively calls gtk_widget_show() on all widgets
     * that are contained in the window, directly or indirectly
     */
    gtk_widget_show_all(window);
}

int main(int argc, char** argv)
{
    GtkApplication *app;
    int status;

    app = gtk_application_new("org.gtk.example", G_APPLICATION_FLAGS_NONE);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app); // Frees GtkApplication object from memory

    return status;
}