from abc import ABC, abstractmethod
import tkinter as tk


class Viewable(ABC):

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__body = None
        return instance

    @property
    def body(self):
        return self.__build()

    def build(self):
        return self.__build()

    def show(self):  # alias for build. used for Views based on a toplevel widget
        return self.__build(toplevel=True)

    def close(self, **kwargs):
        self.__close(**kwargs)

    @abstractmethod
    def _on_start(self):
        pass

    @abstractmethod
    def _on_build(self):
        pass

    @abstractmethod
    def _on_display(self):
        pass

    def _on_map(self, event):
        pass

    def _on_unmap(self, event):
        pass

    @abstractmethod
    def _on_close(self, **kwargs):
        pass

    # ==================== INTERNAL =====================

    def __build(self, toplevel=False):
        if self.__body:
            return self.__body
        self._on_start()
        self.__body = self._on_build()
        self._on_display()
        if not self.__body:
            self.__body = self.__build_default_body(toplevel)
        else:
            self.__body.bind("<Map>", self._on_map, "+")
            self.__body.bind("<Unmap>", self._on_unmap, "+")
            self.__body.bind("<Destroy>", lambda e, self=self: self.__close(event=e), "+")
        return self.__body

    def __build_default_body(self, toplevel):
        if toplevel:
            body = tk.Toplevel()
        else:
            body = tk.Frame()
        tk.Label(body,
                 text="Body missing. Please implement a body to this View " +
                      str(self.__class__)).pack()
        tk.Button(body, text="Close this View", command=self.__close).pack()
        return body

    def __close(self, **kwargs):
        if self.__body:
            self._on_close(**kwargs)
            self.__body.destroy()
            for key, val in self.__dict__.items():
                self.__dict__[key] = None
