#!/usr/bin/env python
import argparse
import logging
import time

import gtk, gobject
import vboxapi

import trayify

log = logging.getLogger(__name__)

vbox_manager = vboxapi.VirtualBoxManager(None, None)
vbox = vbox_manager.vbox


def enum_to_string(constants, enum, element):
    all = constants.all_values(enum)
    for key in all.keys():
        if str(element) == str(all[key]):
            return key

def get_vm_state(machine):
    return enum_to_string(vbox_manager.constants, "MachineState", machine.state)

def start_vm(machine, start_type="gui"):
    session = vbox_manager.mgr.getSessionObject(vbox)
    try:
        progress = machine.launchVMProcess(session, start_type, "")
        progress.waitForCompletion(-1)
    except Exception as e:
        log.error("Error happened")
        raise e
    finally:
        if session.state == vbox_manager.constants.SessionState_Locked:
            session.unlockMachine()

def savestate_vm(machine):
    session = vbox_manager.mgr.getSessionObject(vbox)
    try:
        machine.lockMachine(session, vbox_manager.constants.LockType_Shared)
        session.console.saveState()
    except Exception as e:
        log.error("Error happened")
        raise e
    finally:
        if session.state == vbox_manager.constants.SessionState_Locked:
            session.unlockMachine()

def stop_vm(machine):
    session = vbox_manager.mgr.getSessionObject(vbox)
    try:
        machine.lockMachine(session, vbox_manager.constants.LockType_Shared)
        session.console.powerDown()
    except Exception as e:
        log.error("Error happened")
        raise e
    finally:
        if session.state == vbox_manager.constants.SessionState_Locked:
            session.unlockMachine()

class VboxTrayIcon(object):

    def __init__(self, uuid):
        self.uuid = uuid
        self.machine = vbox.findMachine(uuid)

        self.ico = trayify.initialize('gtk')
        self.ico.create_icon()
        self.ico.set_tooltip(self.uuid)

        self.running_menu = {'Save State': self.savestate_event,
                             'Stop': self.stop_event }
        self.stopped_menu = {'Start': self.start_vm_event,
                             'Start (Headless)': self.start_vm_headless_event }
        self.update()

        gobject.timeout_add_seconds(30, self.update)
        self.ico.start()

    def show_event(self, event):
        self.ico.show_message("The Foo menu item was clicked")

    def start_vm_event(self, event):
        start_vm(self.machine, "gui")
        time.sleep(3)
        self.update()

    def start_vm_headless_event(self, event):
        start_vm(self.machine, "headless")
        time.sleep(3)
        self.update()

    def savestate_event(self, event):
        savestate_vm(self.machine)
        time.sleep(3)
        self.update()

    def stop_event(self, event):
        stop_vm(self.machine)
        time.sleep(3)
        self.update()

    def update(self):
        self.state = get_vm_state(self.machine)
        if self.state == "Running":
            self.ico.set_image_from_stock(gtk.STOCK_YES)
            self.ico.add_menu(self.running_menu)
        elif self.state == "PoweredOff":
            self.ico.set_image_from_stock(gtk.STOCK_NO)
            self.ico.add_menu(self.stopped_menu)
        elif self.state == "Saved":
            self.ico.set_image_from_stock(gtk.STOCK_MEDIA_PAUSE)
            self.ico.add_menu(self.stopped_menu)
        else:
            self.ico.set_image_from_stock(gtk.STOCK_EXECUTE)
        return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("uuid", type=str, help="uuid of the virtualbox vm")
    args = parser.parse_args()
    VboxTrayIcon(uuid=args.uuid)


if __name__ == "__main__":
    main()