import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from signin import *
from mydata import strBase64
from ctypes import *
import _ctypes
from base64 import b64decode
import os


class AccountChecker:
    def __init__(self):
        self.dllname = './tmp.dll'
        self.dll = self.__release_dll()
        self.enc = self.dll.enc
        self.enc.argtypes = (c_char_p, c_char_p, c_char_p, c_int)
        self.enc.restype = c_int

        self.accounts = {
            b'SCTFer': b64decode(b'PLHCu+fujfZmMOMLGHCyWWOq5H5HDN2R5nHnlV30Q0EA')
        }
        self.try_times = 0

    def __release_dll(self):
        with open(self.dllname, 'wb') as f:
            f.write(b64decode(strBase64.encode('ascii')))
        return WinDLL(self.dllname)

    def clean(self):
        _ctypes.FreeLibrary(self.dll._handle)
        if os.path.exists(self.dllname):
            os.remove(self.dllname)

    def _error(self, error_code):
        errormsg = {
            0: 'Unknown Error',
            1: "Memory Error"
        }
        QMessageBox.information(None, "Error", errormsg[error_code], QMessageBox.Abort, QMessageBox.Abort)
        sys.exit(1)

    def __safe(self, username: bytes, password: bytes):
        pwd_safe = b'\x00' * 33
        status = self.enc(username, password, pwd_safe, len(pwd_safe))
        return pwd_safe, status

    def check(self, username, password):
        self.try_times += 1
        if username not in self.accounts:
            return False
        encrypted_pwd, status = self.__safe(username, password)
        if status == 1:
            self.__error(1)
        if encrypted_pwd != self.accounts[username]:
            return False
        self.try_times -= 1
        return True


class SignInWnd(QMainWindow, Ui_QWidget):
    def __init__(self, checker: AccountChecker, parent=None):
        super().__init__(parent)
        self.checker = checker
        self.setupUi(self)
        self.PB_signin.clicked.connect(self.on_confirm_button_clicked)

    @pyqtSlot()
    def on_confirm_button_clicked(self):
        username = bytes(self.LE_usrname.text(), encoding='ascii')
        password = bytes(self.LE_pwd.text(), encoding='ascii')
        if username == b'' or password == b'':
            self.check_input_msgbox()
        else:
            self.msgbox(self.checker.check(username, password))

    def check_input_msgbox(self):
        QMessageBox.information(None, "Error", "Check Your Input!", QMessageBox.Ok, QMessageBox.Ok)

    def msgbox(self, status):
        msg_ex = {
            0: '',
            1: '',
            2: "It's no big deal, try again!",
            3: "Useful information is in the binary, guess what?"
        }
        msg = "Succeeded! Flag is your password" if status else "Failed to sign in\n" + msg_ex[
            self.checker.try_times % 4]
        QMessageBox.information(None, "SCTF2020", msg, QMessageBox.Ok, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    checker = AccountChecker()
    sign_in_wnd = SignInWnd(checker)
    sign_in_wnd.show()
    app.exec()
    checker.clean()
    sys.exit()
