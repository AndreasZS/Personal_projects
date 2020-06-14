GtkBuilder can be used to construct objects that are not widgets, that's why gtk_builder_get_object() is used. Normally you pass a full path to gtk_builder_add_from_file() to make execution independent of current directory.
Common location to install UI descriptions is /usr/share/appname. 
You can embed UI description in source code as a string and use gtk_builder_add_from_string() to load it. But if you keep the UI description in its own file you can make minor adjustments without recompiling and GUI editors like glade can load the file for easy modification. 
