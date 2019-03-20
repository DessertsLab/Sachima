import os
import sys
from multiprocessing import Pool, Process, Queue
from subprocess import PIPE, Popen, call

from sachima.sachima_http_server_flask import app


def mute():
    sys.stdout = open(os.devnull, "w")


def pre():
    WAFFLE_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "Waffle"
    )
    # 判断Waffle目录是否存在  不存在的话git clone
    if not os.path.exists(WAFFLE_DIR):
        os.system(
            "git clone https://github.com/DessertsLab/Waffle.git {}".format(
                WAFFLE_DIR
            )
        )
        os.system("npm install --prefix {}".format(WAFFLE_DIR))
        # 更新sachima到最新版本
        os.system("pip install -U --no-cache-dir sachima")
    else:
        # os.system(
        #     "git -C {0} pull origin master".format(
        #         os.path.join(
        #             os.path.dirname(os.path.realpath(__file__)), "..", "Waffle"
        #         )
        #     )
        # )
        pass


def start_Waffle():
    print(
        "cd {0} & npm install & npm start --prefix {0}".format(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "..", "Waffle"
            )
        )
    )

    os.system(
        "npm start --prefix {0}".format(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "..", "Waffle"
            )
        )
    )


def start_sachima():
    sys.dont_write_bytecode = True
    app.run(host="0.0.0.0", port=80, debug=True)


if __name__ == "__main__":
    pre()

    import subprocess

    cmd_line = "npm start --prefix {0}".format(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", "Waffle"
        )
    )

    w = subprocess.Popen(
        cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    s = subprocess.Popen(
        start_sachima(),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    out = w.wait()
    out2 = s.wait()
