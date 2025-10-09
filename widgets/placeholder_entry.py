from tkinter import ttk


class PlaceholderEntry(ttk.Entry):
    """And Entry widget that shows a placeholder when empty."""

    def __init__(
        self, master=None, placeholder="PLACEHOLDER", color="grey", *args, **kwargs
    ):
        # if textvariable is passed, use callback to hide placeholder when textvariable is set
        if kwargs["textvariable"] is not None:
            tv = kwargs["textvariable"]
            tv.trace_add("write", lambda *args: self._hide_placeholder())

        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["foreground"]

        self.bind("<FocusIn>", lambda event: self._hide_placeholder(True, event))
        self.bind("<FocusOut>", lambda event: self._show_placeholder(event))

        self._show_placeholder()

    def _show_placeholder(self, event=None) -> None:
        if not self.get():
            self.insert(0, self.placeholder)
            self["foreground"] = self.placeholder_color

    def _hide_placeholder(self, delete=False, event=None) -> None:
        fg = str(self["foreground"])
        if fg == self.placeholder_color:
            if delete:
                self.delete(0, "end")
            self["foreground"] = self.default_fg_color
