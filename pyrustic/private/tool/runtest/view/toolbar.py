from pyrustic.viewable import Viewable
import math
import traceback
import tkinter as tk


class Toolbar(Viewable):
    def __init__(self, node_id, parent, callback, log_window_builder):
        self._node_id = node_id
        self._parent = parent
        self._callback = callback
        self._log_window_builder = log_window_builder
        # States variables
        self._toolbar_visible = True
        self._is_running = False
        self._is_waiting = False
        self._time_elapsed = 0
        self._count_tests = 0
        self._count_tests_started = 0
        self._count_errors = 0
        self._count_sub_test_errors = 0
        self._count_sub_test_failures = 0
        self._count_failures = 0
        self._count_skips = 0
        self._count_unexpected_successes = 0
        self._count_expected_failures = 0
        # StringVar
        self._state_stringvar = tk.StringVar()
        self._time_elapsed_stringvar = tk.StringVar()
        self._count_tests_stringvar = tk.StringVar(value="0")
        self._percent_stringvar = tk.StringVar(value="0%")
        self._count_tests_started_stringvar = tk.StringVar()
        self._error_stringvar = tk.StringVar()
        self._sub_test_error_stringvar = tk.StringVar()
        self._sub_test_failure_stringvar = tk.StringVar()
        self._failure_stringvar = tk.StringVar()
        self._skip_stringvar = tk.StringVar()
        self._expected_failure_stringvar = tk.StringVar()
        self._unexpected_success_stringvar = tk.StringVar()
        self._live_info_stringvar = tk.StringVar()
        # IntVar
        self._failfast_intvar = tk.IntVar()
        self._verbose_intvar = tk.IntVar(value=1)
        # body
        self._body = None
        # frame
        self._frame_top = self._frame_bottom = None
        self._frame_top_left = self._frame_top_right = self._frame_bottom_1 = None
        self._frame_bottom_2 = self._frame_bottom_3 = None
        # Buttons
        self._btn_run = self._btn_rerun = self._btn_stop = self._btn_cancel = None
        self._btn_log = self._btn_clean = None
        # Checkbutton
        self._checkbutton_failfast = self._checkbutton_verbose = None
        # Labels
        self._label_state = self._label_testing_passed = self._label_testing_failed = None
        self._label_time_elapsed = self._label_count_tests = None
        self._label_count_tests_completed = self._label_percent =  None
        self._label_error = self._label_sub_test_error = self._label_failure = None
        self._label_sub_test_failure = self._label_skip = None
        self._label_expected_failure = self._label_unexpected_success = None
        self._live_info_label = None
        # raw log
        self._raw_log = []
        # log
        self._log = None

    # ========================================
    #             PROPERTIES
    # ========================================
    @property
    def is_visible(self):
        return self._toolbar_visible

    @property
    def count_tests(self):
        return self._count_tests

    @count_tests.setter
    def count_tests(self, val):
        self._count_tests = val
        val = "{} test{}".format(val, "s" if val > 1 else "")
        self._count_tests_stringvar.set(val)

    # ========================================
    #             PUBLIC METHODS
    # ========================================
    def show_or_hide(self):
        if self._toolbar_visible:
            self._body.grid_remove()
            self._toolbar_visible = False
        else:
            self._body.grid()
            self._toolbar_visible = True

    def set_running_state(self):
        self._is_running = True
        self._state_stringvar.set("Running...")
        if self._is_waiting:
            self._is_waiting = False
        # remove widgets
        self._reset_toolbar()
        # set btn stop
        self._btn_stop.grid()
        # set label state
        self._label_state.grid()
        # set label count_tests_completed
        self._label_count_tests_completed.grid()
        # set label Percent
        self._label_percent.grid()
        # set live info
        if self._verbose_intvar.get() == 1:
            self._frame_bottom.grid()
            self._frame_bottom_1.grid()
            self._live_info_label.grid()

    def set_waiting_state(self):
        self._is_waiting = True
        self._state_stringvar.set("Waiting...")
        # remove widgets
        self._reset_toolbar()
        # set btn cancel
        self._btn_cancel.grid()
        # set label Current state
        self._label_state.grid()
        # set label Count_tests
        self._label_count_tests.grid()

    def set_stop_state(self, was_successful, log):
        self._raw_log = log
        self._is_running = False
        # set label testing failed or label testing passed
        if was_successful:
            self._label_testing_passed.grid()
        else:
            self._label_testing_failed.grid()
        # set time elapsed
        self._label_time_elapsed.grid()
        # remove state label
        self._label_state.grid_remove()
        # remove frame_bottom_1
        self._frame_bottom_1.grid_remove()
        # conditionally remove frame_bottom_2 and frame_bottom_3
        remove_frame_bottom_2 = True
        remove_frame_bottom_3 = True
        for x in (self._count_errors, self._count_sub_test_errors,
                  self._count_failures, self._count_sub_test_failures):
            if x != 0:
                remove_frame_bottom_2 = False
        for x in (self._count_unexpected_successes, self._count_expected_failures,
                  self._count_skips):
            if x != 0:
                remove_frame_bottom_3 = False
        if remove_frame_bottom_2:
            self._frame_bottom_2.grid_remove()
        if remove_frame_bottom_3:
            self._frame_bottom_3.grid_remove()
        if remove_frame_bottom_2 and remove_frame_bottom_3:
            self._frame_bottom.grid_remove()
        # remove stop button
        self._btn_stop.grid_remove()
        # set rerun button
        self._btn_rerun.grid()
        # set log button
        self._btn_log.grid()
        # set clean button
        self._btn_clean.grid()


    def notify_time_elapsed(self, time_elapsed):
        self._time_elapsed = math.floor(time_elapsed * 10 ** 3) / 10 ** 3
        self._time_elapsed_stringvar.set(str("{}s".format(self._time_elapsed)))

    def notify_start_test(self, test):
        self._count_tests_started += 1
        count_tests_started = "{}/{}".format(self._count_tests_started, self._count_tests)
        self._live_info_stringvar.set(">>> " + str(test))
        self._count_tests_started_stringvar.set(count_tests_started)
        percent = int((self._count_tests_started / self._count_tests) * 100)
        percent = "{}%".format(percent)
        self._percent_stringvar.set(percent)

    def notify_stop_test(self, test):
        pass

    def notify_add_error(self, test, err):
        self._count_errors += 1
        if self._verbose_intvar.get() != 1:
            return
        count_errors = "{} error{}".format(self._count_errors,
                                           "s" if self._count_errors > 1 else "")
        self._error_stringvar.set(count_errors)
        self._frame_bottom.grid()
        self._frame_bottom_2.grid()
        self._label_error.grid()

    def notify_add_failure(self, test, err):
        self._count_failures += 1
        if self._verbose_intvar.get() != 1:
            return
        count_failures = "{} failure{}".format(self._count_failures,
                                           "s" if self._count_failures > 1 else "")
        self._failure_stringvar.set(count_failures)
        self._frame_bottom.grid()
        self._frame_bottom_2.grid()
        self._label_failure.grid()

    def notify_add_success(self, test):
        pass

    def notify_add_skip(self, test, reason):
        self._count_skips += 1
        if self._verbose_intvar.get() != 1:
            return
        self._skip_stringvar.set("{} skipped".format(self._count_skips))
        self._frame_bottom.grid()
        self._frame_bottom_3.grid()
        self._label_skip.grid()

    def notify_add_expected_failure(self, test, err):
        self._count_expected_failures += 1
        if self._verbose_intvar.get() != 1:
            return
        count_expected_failures = ("{} expected-failure{}".
                                   format(self._count_expected_failures,
                            "s" if self._count_expected_failures > 1 else ""))
        self._expected_failure_stringvar.set(count_expected_failures)
        self._frame_bottom.grid()
        self._frame_bottom_3.grid()
        self._label_expected_failure.grid()

    def notify_add_unexpected_success(self, test):
        self._count_unexpected_successes += 1
        if self._verbose_intvar.get() != 1:
            return
        count_unexpected_successes = ("{} unexpected-success{}".
                                      format(self._count_unexpected_successes,
                            "es" if self._count_unexpected_successes > 1 else ""))
        self._unexpected_success_stringvar.set(count_unexpected_successes)
        self._frame_bottom.grid()
        self._frame_bottom_3.grid()
        self._label_unexpected_success.grid()

    def notify_add_sub_test(self, test, subtest, outcome):
        self._live_info_stringvar.set("Currently on: " + str(subtest))
        if not outcome:
            return
        if issubclass(outcome[0], test.failureException):
            self._count_sub_test_failures += 1
            if self._verbose_intvar.get() != 1:
                return
            count_sub_test_failures = ("{} sub-test-failure{}"
                                       .format(self._count_sub_test_failures,
                                    "s" if self._count_sub_test_failures > 1 else ""))
            self._sub_test_failure_stringvar.set(count_sub_test_failures)
            self._frame_bottom_2.grid()
            self._label_sub_test_failure.grid()
        else:
            self._count_sub_test_errors += 1
            if self._verbose_intvar.get() != 1:
                return
            count_sub_test_errors = ("{} sub-test-error{}"
                                       .format(self._count_sub_test_errors,
                                               "s" if self._count_sub_test_errors > 1 else ""))
            self._sub_test_error_stringvar.set(count_sub_test_errors)
            self._frame_bottom_2.grid()
            self._label_sub_test_error.grid()


    # ========================================
    #       VIEWABLE METHODS IMPLEMENTATION
    # ========================================

    def _on_build(self):
        self._body = tk.Frame(self._parent, name="runtestToolbar")
        self._body.grid(pady=5, sticky="w")
        # ============== frames ================
        self._frame_top = tk.Frame(self._body)
        self._frame_top_left = tk.Frame(self._frame_top)
        self._frame_top_right = tk.Frame(self._frame_top)
        self._frame_bottom = tk.Frame(self._body)
        self._frame_bottom_1 = tk.Frame(self._frame_bottom)
        self._frame_bottom_2 = tk.Frame(self._frame_bottom)
        self._frame_bottom_3 = tk.Frame(self._frame_bottom)
        # frame config
        # grid frames
        self._frame_top.grid(row=0, column=0, sticky="w")
        self._frame_top_left.grid(row=0, column=0, sticky="w")
        self._frame_top_right.grid(row=0, column=1, sticky="w")
        self._frame_bottom.grid(row=1, column=0, sticky="w")
        self._frame_bottom_1.grid(row=1, column=0, sticky="w",
                                  pady=(5, 0), padx=(0, 10))
        self._frame_bottom_2.grid(row=2, column=0, sticky="w",
                                  pady=(5, 0))
        self._frame_bottom_3.grid(row=3, column=0, sticky="w",
                                  pady=(5, 0))
        # =========== buttons =============
        # btn run
        self._btn_run = tk.Button(self._frame_top_left,
                                  name="buttonRun",
                                  text="Run",
                                  command=self._on_run_clicked)
        # btn rerun
        self._btn_rerun = tk.Button(self._frame_top_left,
                                    name="buttonRerun",
                                    text="Rerun",
                                    command=self._on_rerun_clicked)
        # btn stop
        self._btn_stop = tk.Button(self._frame_top_left,
                                   name="buttonStop",
                                   text="Stop",
                                   command=self._on_stop_clicked)
        # btn cancel
        self._btn_cancel = tk.Button(self._frame_top_left,
                                     name="buttonCancel",
                                     text="Cancel",
                                     command=self._on_cancel_clicked)
        # btn log
        self._btn_log = tk.Button(self._frame_top_left,
                                  name="buttonLog",
                                  text="Log",
                                  command=self._on_log_clicked)
        # btn clean
        self._btn_clean = tk.Button(self._frame_top_left,
                                    name="buttonClean",
                                    text="x",
                                    command=self._on_clean_clicked)
        # grid buttons
        for i, x in enumerate((self._btn_run, self._btn_rerun,
                            self._btn_stop, self._btn_cancel,
                            self._btn_log, self._btn_clean)):
            x.grid(row=0, column=i, padx=(0, 10))
        # =============== right-side of top frame ============
        # label state
        self._label_state = tk.Label(self._frame_top_right,
                                     textvariable=self._state_stringvar)
        # label testing passed
        self._label_testing_passed = tk.Label(self._frame_top_right,
                                              name="labelTestingPassed",
                                              text="Testing passed !")
        # label testing failed
        self._label_testing_failed = tk.Label(self._frame_top_right,
                                              name="labelTestingFailed",
                                              text="Testing failed !")
        # label duration
        self._label_time_elapsed = tk.Label(self._frame_top_right, textvariable=self._time_elapsed_stringvar)
        # label count_tests
        self._label_count_tests = tk.Label(self._frame_top_right,
                                           textvariable=self._count_tests_stringvar)
        # label count_tests_completed
        self._label_count_tests_completed = tk.Label(self._frame_top_right,
                                                     textvariable=self._count_tests_started_stringvar)
        # label percent
        self._label_percent = tk.Label(self._frame_top_right, textvariable=self._percent_stringvar)
        # checkbutton failfast
        self._checkbutton_failfast = tk.Checkbutton(self._frame_top_right,
                                                    text="Fail-Fast",
                                                    variable=self._failfast_intvar,
                                                    onvalue=1, offvalue=0)
        # checkbutton verbose
        self._checkbutton_verbose = tk.Checkbutton(self._frame_top_right,
                                                   text="Verbose",
                                                   variable=self._verbose_intvar,
                                                   onvalue=1, offvalue=0)
        # grid
        for i, x in enumerate((self._label_state, self._label_testing_passed,
                               self._label_testing_failed, self._label_time_elapsed,
                               self._label_count_tests, self._label_count_tests_completed,
                               self._label_percent, self._checkbutton_failfast,
                               self._checkbutton_verbose)):
            x.grid(row=0, column=i, padx=(0, 10))
        # =============== second stage frame elements ==============
        # label live info
        self._live_info_label = tk.Label(self._frame_bottom_1, textvariable=self._live_info_stringvar)
        # grid
        self._live_info_label.grid(row=0, column=0)
        # =============== third stage frame elements ==============
        # label error
        self._label_error = tk.Label(self._frame_bottom_2, textvariable=self._error_stringvar)
        # label sub_test error
        self._label_sub_test_error = tk.Label(self._frame_bottom_2,
                                              textvariable=self._sub_test_error_stringvar)
        # label failure
        self._label_failure = tk.Label(self._frame_bottom_2,
                                       textvariable=self._failure_stringvar)
        # label sub_test failure
        self._label_sub_test_failure = tk.Label(self._frame_bottom_2,
                                                textvariable=self._sub_test_failure_stringvar)
        # grid
        for i, x in enumerate((self._label_error, self._label_sub_test_error,
                               self._label_failure, self._label_sub_test_failure)):
            x.grid(row=0, column=i, padx=(0, 20))
        # =============== fourth stage frame elements ==============
        # label unexpected success
        self._label_unexpected_success = tk.Label(
            self._frame_bottom_3, textvariable=self._unexpected_success_stringvar)
        # label expected failure
        self._label_expected_failure = tk.Label(
            self._frame_bottom_3, textvariable=self._expected_failure_stringvar)
        # label skip
        self._label_skip = tk.Label(self._frame_bottom_3, textvariable=self._skip_stringvar)
        # grid
        for i, x in enumerate((self._label_unexpected_success, self._label_expected_failure,
                               self._label_skip)):
            x.grid(row=0, column=i, padx=(0, 20))
        # ====================================================
        # reset
        self._reset_toolbar()
        self._install_default_widgets()
        return self._body

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    # ========================================
    #             PRIVATE METHODS
    # ========================================
    def _on_run_clicked(self):
        self._callback.on_run_clicked(self._node_id,
                                      self._failfast_intvar.get())

    def _on_rerun_clicked(self):
        self._on_clean_clicked()
        self._callback.on_run_clicked(self._node_id, self._failfast_intvar.get())

    def _on_stop_clicked(self):
        self._callback.on_stop_clicked(self._node_id)

    def _on_cancel_clicked(self):
        self._is_waiting = False
        self._reset_toolbar()
        self._install_default_widgets()
        self._callback.on_cancel_clicked(self._node_id)

    def _on_clean_clicked(self):
        self._reset_data()
        self._reset_toolbar()
        self._install_default_widgets()

    def _reset_toolbar(self):
        for x in (*self._frame_top_left.winfo_children(),
                  *self._frame_top_right.winfo_children(),
                  *self._frame_bottom_1.winfo_children(),
                  *self._frame_bottom_2.winfo_children(),
                  *self._frame_bottom_3.winfo_children(),
                  self._frame_bottom_1,
                  self._frame_bottom_2,
                  self._frame_bottom_3,
                  self._frame_bottom):
            x.grid_remove()

    def _reset_data(self):
        self._raw_log = []
        self._log = None
        self._percent_stringvar.set("0%")
        self._state_stringvar.set("")
        self._live_info_stringvar.set("")
        self._time_elapsed = 0
        self._count_tests_started = 0
        self._count_errors = 0
        self._count_sub_test_errors = 0
        self._count_sub_test_failures = 0
        self._count_failures = 0
        self._count_skips = 0
        self._count_unexpected_successes = 0
        self._count_expected_failures = 0

    def _install_default_widgets(self):
        # install btn run, label count_tests, checkbuttons failfast and verbose
        self._btn_run.grid()
        self._label_count_tests.grid()
        self._checkbutton_failfast.grid()
        self._checkbutton_verbose.grid()

    def _on_log_clicked(self):
        log_window = self._log_window_builder.build(self._body, self._get_log())

    def _get_log(self):
        if self._log is not None:
            return self._log
        text = ""
        line_separator = "\n\n{}\n\n".format("-" * 75)
        format_error = lambda err: "".join(traceback.format_exception(*err))
        for x in self._raw_log:
            event = x["event"]
            if event == "start_test_run":
                text += (" "*25) + "===== START TEST =====\n"
                text += line_separator
            elif event == "stop_test_run":
                text += (" "*25) + "===== STOP TEST =====\n"
            elif event == "add_error":
                text += "*** ERROR\n"
                text += "{}\n\n".format(x["test"])
                text += format_error(x["err"])
                text += line_separator
            elif event == "add_failure":
                text += "*** FAILURE\n"
                text += "{}\n\n".format(x["test"])
                text += format_error(x["err"])
                text += line_separator
            elif event == "add_skip":
                text += "*** SKIP\n"
                text += "{}\n\n".format(x["test"])
                text += "Reason: " + x["reason"]
                text += line_separator
            elif event == "add_expected_failure":
                text += "*** EXPECTED FAILURE\n"
                text += "{}\n\n".format(x["test"])
                text += format_error(x["err"])
                text += line_separator
            elif event == "add_unexpected_success":
                text += "*** UNEXPECTED SUCCESS\n"
                text += "{}\n\n".format(x["test"])
                text += line_separator
            elif event == "add_sub_test":
                outcome = x["outcome"]
                test = x["test"]
                if outcome is not None:
                    if issubclass(outcome[0], test.failureException):
                        text += "*** SUB-TEST FAILURE\n"
                    else:
                        text += "*** SUB-TEST ERROR\n"
                    text += "{}\n\n".format(x["sub_test"])
                    text += format_error(outcome)
                    text += line_separator
        self._log = text
        return self._log
