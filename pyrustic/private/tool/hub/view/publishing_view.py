from pyrustic.viewable import Viewable
from pyrustic.widget.confirm import Confirm
from pyrustic.widget.toast import Toast
from pyrustic import tkmisc
import tkinter as tk
import os.path
from pyrustic.private.tool.hub.view.failure_view import FailureView


class PublishingView(Viewable):
    def __init__(self, master, main_view, main_host, asset_version):
        self._master = master
        self._main_view = main_view
        self._main_host = main_host
        self._asset_version = asset_version
        # stringvars and intvars
        self._strvar_target = tk.StringVar()
        self._strvar_owner = tk.StringVar()
        self._strvar_repo = tk.StringVar()
        self._strvar_target_commitish = tk.StringVar()
        self._strvar_tag_name = tk.StringVar()
        self._strvar_description = tk.StringVar()
        self._strvar_release_name = tk.StringVar()
        self._intvar_prerelease = tk.IntVar(value=0)
        self._intvar_draft = tk.IntVar(value=0)
        self._strvar_asset_name = tk.StringVar()
        self._strvar_asset_label = tk.StringVar()
        # cache toast "Processing..."
        self._cache_toast_processing = None
        # asset path
        self._asset_path = None
        # target project
        self._target_project = None

    def _on_build(self):
        self._body = tk.Toplevel()
        self._body.title("Publishing")
        self._body.resizable(0, 0)
        # header
        self._set_header(self._body)
        # frame_form
        frame_form = tk.Frame(self._body, name="frame_form")
        frame_form.pack(padx=10, pady=20, expand=1, fill=tk.BOTH)
        frame_form.columnconfigure(0, pad=5)
        frame_form.columnconfigure(1, pad=5)
        frame_form.rowconfigure(0, pad=10)
        frame_form.rowconfigure(1, pad=10)
        frame_form.rowconfigure(2, pad=10)
        frame_form.rowconfigure(3, pad=10)
        # owner
        self._set_widgets_owner(frame_form)
        # repo
        self._set_widgets_repo(frame_form)
        # target_commitish
        self._set_widgets_target_commitish(frame_form)
        # tag_name
        self._set_widgets_tag_name(frame_form)
        # release name
        self._set_widgets_release_name(frame_form)
        # archive format
        self._set_widgets_archive_format(frame_form)
        # asset_name
        self._set_widgets_asset_name(frame_form)
        # asset_label
        self._set_widgets_asset_label(frame_form)
        # description
        self._set_widgets_description(frame_form)
        # label to describe mandatory field
        self._set_widgets_describe_mandatory_fields(frame_form)
        # footer
        self._set_widgets_footer(self._body)

    def _on_display(self):
        self._populate()

    def _on_destroy(self):
        pass

    def _toplevel_geometry(self):
        tkmisc.center_window(self._body)
        tkmisc.dialog_effect(self._body)

    # ====================================
    #               PRIVATE
    # ====================================
    def _set_header(self, parent):
        # == top area
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X)
        # label 'target project'
        label_target_project = tk.Label(frame, name="label_project",
                                        text="Project:")
        label_target_project.pack(side=tk.LEFT)
        # entry
        entry_path = tk.Entry(frame, name="entry_project",
                              state="readonly",
                              textvariable=self._strvar_target)
        entry_path.pack(side=tk.LEFT, expand=1, fill=tk.X)

    def _set_widgets_owner(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=0, column=0, sticky="w")
        # label
        label_owner = tk.Label(frame, text="Owner")
        label_owner.pack(anchor="w")
        # entry
        entry_owner = tk.Entry(frame, width=20,
                               textvariable=self._strvar_owner,
                              state="readonly")
        entry_owner.pack(anchor="w")

    def _set_widgets_repo(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=1, column=0, sticky="w")
        # label
        label_repo = tk.Label(frame, text="Repository *")
        label_repo.pack(anchor="w")
        # entry
        entry_repo = tk.Entry(frame, width=20,
                              textvariable=self._strvar_repo)
        entry_repo.pack(anchor="w")

    def _set_widgets_target_commitish(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=2, column=0, sticky="w")
        # label
        label_target_commitish = tk.Label(frame, text="Target commitish")
        label_target_commitish.pack(anchor="w")
        # entry
        entry_target_commitish = tk.Entry(frame, width=20,
                                          textvariable=self._strvar_target_commitish)
        entry_target_commitish.pack(anchor="w")

    def _set_widgets_tag_name(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=0, column=1, sticky="w")
        # label
        label_tag_name = tk.Label(frame, text="Tag name *")
        label_tag_name.pack(anchor="w")
        # entry
        entry_tag_name = tk.Entry(frame, width=20,
                                  textvariable=self._strvar_tag_name)
        entry_tag_name.pack(anchor="w")

    def _set_widgets_description(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=3, column=0, columnspan=3, sticky="we")
        # label
        label_description = tk.Label(frame, text="Description")
        label_description.pack(anchor="w")
        # text
        self._text_description = tk.Text(frame, name="text_description",
                                         height=5, width=40)
        self._text_description.pack(anchor="w", fill=tk.X)

    def _set_widgets_release_name(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=1, column=1, sticky="w")
        # label
        label_release_name = tk.Label(frame, text="Release name")
        label_release_name.pack(anchor="w")
        # entry
        entry_release_name = tk.Entry(frame, width=20,
                                      textvariable=self._strvar_release_name)
        entry_release_name.pack(anchor="w")

    def _set_widgets_archive_format(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=2, column=1, sticky="w")
        # label
        label_archive_format = tk.Label(frame, text="Archive format")
        label_archive_format.pack(anchor="w")
        # entry
        strvar = tk.StringVar(value="zip")
        entry_archive_format = tk.Entry(frame, width=20,
                                        textvariable=strvar,
                                        state="readonly")
        entry_archive_format.pack(anchor="w")

    def _set_widgets_asset_name(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=0, column=2, sticky="w")
        # label
        label_asset_name = tk.Label(frame, text="Asset name")
        label_asset_name.pack(anchor="w")
        # entry
        entry_asset_name = tk.Entry(frame, width=20,
                                    textvariable=self._strvar_asset_name)
        entry_asset_name.pack(anchor="w")

    def _set_widgets_asset_label(self, parent):
        # frame
        frame = tk.Frame(parent)
        frame.grid(row=1, column=2, sticky="w")
        # label
        label_asset_label = tk.Label(frame, text="Asset label")
        label_asset_label.pack(anchor="w")
        # entry
        entry_asset_label = tk.Entry(frame, width=20,
                                     textvariable=self._strvar_asset_label)
        entry_asset_label.pack(anchor="w")

    def _set_widgets_describe_mandatory_fields(self, parent):
        label = tk.Label(parent, name="label_mandatory",
                         text="* Mandatory fields")
        label.grid(row=4, column=0, sticky="w", pady=10)

    def _set_widgets_footer(self, parent):
        frame_footer = tk.Frame(parent)
        frame_footer.pack(fill=tk.X, padx=2, pady=2)
        button_publishing = tk.Button(frame_footer, name="button_confirm",
                                    text="Publish",
                                    command=self._on_click_publishing)
        button_publishing.pack(side=tk.RIGHT)
        button_cancel = tk.Button(frame_footer, name="button_cancel",
                                  text="Cancel",
                                  command=self._on_click_cancel)
        button_cancel.pack(side=tk.RIGHT, padx=(20, 2))
        # checkbutton Draft
        checkbutton_run_scripts = tk.Checkbutton(frame_footer, text="Draft",
                                               variable=self._intvar_draft)
        checkbutton_run_scripts.pack(side=tk.LEFT, padx=(0, 10))
        # checkbutton pre-release
        checkbutton_prerelease = tk.Checkbutton(frame_footer, text="Pre-release",
                                                variable=self._intvar_prerelease)
        checkbutton_prerelease.pack(side=tk.LEFT)

    def _on_click_cancel(self):
        self.destroy()

    def _on_click_publishing(self):
        if not self._check_mandatory_field():
            return
        confirm = Confirm(self._body, title="Confirmation",
                          header="Ready to publish your project",
                          message="Do you want to continue ?")
        confirm.build_wait()
        if not confirm.ok:
            return
        owner = self._strvar_owner.get()
        repo = self._strvar_repo.get()
        name = self._strvar_release_name.get()
        tag_name = self._strvar_tag_name.get()
        target_commitish = self._strvar_target_commitish.get()
        description = self._text_description.get("1.0","end-1c")
        prerelease = True if self._intvar_prerelease.get() == 1 else False
        draft = True if self._intvar_draft.get() == 1 else False
        asset_name = self._strvar_asset_name.get()
        asset_label = self._strvar_asset_label.get()
        self._asset_path = os.path.join(self._target_project,
                                        "pyrustic_data", "dist",
                                        "{}.zip".format(self._asset_version))
        # threadium stuff
        threadium = self._main_view.threadium
        host = self._main_host.publishing
        host_args = (owner, repo, name, tag_name, target_commitish,
                     description, prerelease, draft,
                     self._asset_path, asset_name, asset_label)
        consumer = self._notify_publishing_response
        threadium.task(host, args=host_args, consumer=consumer)
        self._cache_toast_processing = Toast(self._body, message="Processing...",
                                             duration=None)
        self._cache_toast_processing.build()

    def _check_mandatory_field(self):
        if self._strvar_repo.get() == "":
            toast = Toast(self._body, message="Please set the repository name")
            toast.build()
            return False
        if self._strvar_tag_name.get() == "":
            toast = Toast(self._body, message="Please set the tag name")
            toast.build()
            return False
        return True

    def _populate(self):
        self._target_project = self._main_host.target_project()
        data = self._main_host.about_target_project()
        target = data["target"]
        project_name = data["project_name"]
        version = self._asset_version
        owner = self._main_host.login
        default_target_commitish = "master"
        # target
        self._strvar_target.set(target)
        # owner
        self._strvar_owner.set(owner)
        # repo
        self._strvar_repo.set(project_name)
        # target commitish
        self._strvar_target_commitish.set(default_target_commitish)
        # tag name
        self._strvar_tag_name.set("v{}".format(version))
        # release name
        self._strvar_release_name.set("v{}".format(version))
        # asset name
        cache = "{}-v{}-released-by-{}.zip".format(project_name, version, owner)
        self._strvar_asset_name.set(cache)
        # asset label
        self._strvar_asset_label.set("Download the release")
        # description
        owner = self._strvar_owner.get()
        repo = self._strvar_repo.get()
        pyrustic_link = "https://github.com/pyrustic/pyrustic#readme"
        cache = "To install this app on your computer:\n\n"
        cache += "```bash\n"
        cache += "$ pip install geet\n"
        cache += "$ python3 -m geet {}/{}\n".format(owner, repo)
        cache += "```\n\n"
        cache += "To run this app:\n\n"
        cache += "```bash\n"
        cache += "$ python3 -m geet run {}/{}\n".format(owner, repo)
        cache += "```\n\n"
        cache += "To install and or run in a convenient loop:\n\n"
        cache += "```bash\n"
        cache += "$ python3 -m geet\n"
        cache += "Welcome to Geet !"
        cache += "(geet) {}/{}\n".format(owner, repo)
        cache += "...\n"
        cache += "(geet) run {}/{}\n".format(owner, repo)
        cache += "```\n\n"
        cache += "Packaged and released with [Pyrustic]({}).".format(pyrustic_link)
        self._text_description.insert("1.0", cache)

    def _notify_publishing_response(self, data):
        if self._cache_toast_processing:
            self._cache_toast_processing.destroy()
            self._cache_toast_processing = None
        meta_code = data["meta_code"]
        status_code = data["status_code"]
        status_text = data["status_text"]
        message = "Successfully published"
        messages = {0: "Successfully published !",
                    1: "Failed to cache the target project\n{}".format(data["data"]),
                    2: "Tests failed\n{}".format(data["data"]),
                    3: "Failed to execute prolog\n{}".format(data["data"]),
                    4: "Failed to zip\n{}".format(data["data"]),
                    5: "Failed to create release\n{}".format(status_text),
                    6: "Failed to upload zip\n{}".format(status_text),
                    7: "Failed to execute epilog\n{}".format(data["data"])}
        message = messages[meta_code]
        if meta_code == 0:
            toast = Toast(self._body, message=message)
            toast.build_wait()
            data = (self._strvar_owner.get(), self._strvar_repo.get())
            self._main_view.central_view.add_node(*data)
            self.destroy()
        else:
            failure_view = FailureView(self._body, self._main_view,
                                       self._main_host, message)
            failure_view.build_wait()
