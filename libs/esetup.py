import sys
import os
import time
import pip
import base64

EPKGVERSION = "1.2"
output = False


def log(*args):
    if output:
        print(*args)


class epkg:
    def __init__(self, name, author, version, describe, email="NaN", website="NaN", pyver=sys.version.split(" ")[0]):
        self.name = name
        self.author = author
        self.version = version
        self.website = website
        self.email = email
        self.describe = describe
        self.pyver = pyver
        self.pkgfiles = []
        self.pkglibs = []
        self.initFile = ""

    def addFile(self, path):
        self.pkgfiles.append(path)

    def addLib(self, pkg):
        self.pkglibs.append(pkg)

    def setInitFile(self, path):
        self.initFile = path

    def readfile(self, path):
        with open(path, "rb") as f:
            return f.read()

    def addFolder(self, path, only_Folder=False):
        if not only_Folder:
            for root, dirs, files in os.walk(path):
                for file in files:
                    self.addFile(os.path.join(root, file))
            else:
                self.addFile(path)
        else:
            self.addFile(path)

    def pack(self, output="."):
        CONTENT = ""
        for i in self.pkgfiles:
            if not os.path.isdir(i):
                file = f"""
// START //
> {i}
{self.readfile(i)}
// END //
                """
                CONTENT += file
            else:
                file = f"""
// START //
+ {i}
// END //
                                """
                CONTENT += file
        self.pkgdat = f"""
// INFO //
# NAME #
{self.name}
## NAME ##
# AUTHOR #
{self.author}
## AUTHOR ##
# VERSION #
{self.version}
## VERSION ##
# EMAIL #
{self.email}
## EMAIL ##
# DESCRIBE #
{self.describe}
## DESCRIBE ##
# WEBSITE #
{self.website}
## WEBSITE ##
# PYVERSION #
{self.pyver}
## PYVERSION ##
# PKGLIBS #
{self.pkglibs}
## PKGLIBS ##
// INFO //
// CONTENT //
{CONTENT}
// CONTENT //
        """
        if self.initFile:
            self.pkgdat += f"""
// INITFILE //
{self.readfile(self.initFile)}
// INITFILE //
            """
        header = f"""
/// EPKG DESCRIBE ///
EPKG VERSION:{EPKGVERSION}
PACK TIME:{time.time()}
PYTHON VERSION:{sys.version}
/// EPKG DESCRIBE ///
"""
        step = 0
        ecode = base64.b64encode(self.pkgdat.encode("utf-8")).decode("utf-8")
        rcode = ""
        for i in ecode:
            rcode += i + " "
            step += 1
            if step == 20:
                step = 0
                rcode += "\n"
        result = header + "/// ECODE ///\n" + rcode + "\n/// ECODE ///"
        with open(f"{output}/{self.name}-{self.version}-py{self.pyver}.epkg", "w", encoding="utf-8") as f:
            f.write(result)


def version10(pkgdat):
    if pkgdat[1].strip() == "/// EPKG DESCRIBE ///":
        log("PACK INFO")
        log(pkgdat[2].strip())
        log(pkgdat[3].strip())
        log(pkgdat[4].strip())
        log("UNPACK EPKG...")
        infostart = pkgdat.index("// INFO //\n")
        infostop = pkgdat[pkgdat.index("// INFO //\n") + 1:].index("// INFO //\n")
        info = pkgdat[infostart + 1:infostop]
        name = info[info.index("# NAME #\n") + 1]
        author = info[info.index("# AUTHOR #\n") + 1]
        version = info[info.index("# VERSION #\n") + 1]
        email = info[info.index("# EMAIL #\n") + 1]
        website = info[info.index("# WEBSITE #\n") + 1]
        describe = info[info.index("# DESCRIBE #\n") + 1:info.index("## DESCRIBE ##\n")]
        log("Name:", name.strip())
        log("Author:", author.strip())
        log("Version:", version.strip())
        log("Email:", email.strip())
        log("Website:", website.strip())
        log("Describe:")
        log("".join(describe))
        log("INSTALL LIBS")
        pkglibs = pkgdat[pkgdat.index("# PKGLIBS #\n") + 1]
        for i in eval(pkglibs.strip()):
            pip.main(["install", i])
        log("UNPACK FILE...")
        if "// INITFILE //\n" in pkgdat:
            log("RUN INITFILE")
            filestart = pkgdat.index("// INITFILE //\n") + 1
            filestop = pkgdat.index("// INITFILE //\n", filestart)
            file = pkgdat[filestart:filestop]
            exec("".join(file))
        log("UNPACK CONTENT")
        log("LOCATE...")
        cstart = pkgdat.index("// CONTENT //\n") + 1
        cstop = pkgdat.index("// CONTENT //\n", cstart)
        contents = pkgdat[cstart:cstop]
        log("SPLIT FILE...")
        targets = []
        files = []
        for i in range(0, len(contents)):
            if contents[i] == "// START //\n":
                targets.append(i + 1)
            elif contents[i] == "// END //\n":
                targets.append(i)
        for i in range(0, len(targets), 2):
            files.append(contents[targets[i]:targets[i + 1]])
        for i in files:
            path, name = os.path.split(i[0].replace("> ", "").strip())
            if not os.path.exists(path):
                log(f"CREATE DIR {path}")
                os.makedirs(path)
            log(f"WRITE FILE {name}")
            with open(path + "/" + name, "w", encoding="utf-8") as f:
                f.write("".join(i[1:]))

    else:
        log("!!!ERROR EPKG FILE!!!")


def version11(pkgdat):
    if pkgdat[1].strip() == "/// EPKG DESCRIBE ///":
        log("PACK INFO")
        log(pkgdat[2].strip())
        log(pkgdat[3].strip())
        log(pkgdat[4].strip())
        log("DECODE ECODE...")
        ecstart = pkgdat.index("/// ECODE ///\n")
        ecstop = pkgdat.index("/// ECODE ///", ecstart)
        ecode = pkgdat[ecstart + 1:ecstop]
        rcode = base64.b64decode("".join(ecode).replace(" ", "").replace("\n", "")).decode("utf-8")
        pkgdat[ecstart:] = ""
        for i in rcode.splitlines():
            pkgdat.append(i + "\n")
        log("UNPACK EPKG...")
        infostart = pkgdat.index("// INFO //\n")
        infostop = pkgdat.index("// INFO //\n", infostart + 1)
        info = pkgdat[infostart + 1:infostop]
        name = info[info.index("# NAME #\n") + 1]
        author = info[info.index("# AUTHOR #\n") + 1]
        version = info[info.index("# VERSION #\n") + 1]
        email = info[info.index("# EMAIL #\n") + 1]
        website = info[info.index("# WEBSITE #\n") + 1]
        describe = info[info.index("# DESCRIBE #\n") + 1:info.index("## DESCRIBE ##\n")]
        log("Name:", name.strip())
        log("Author:", author.strip())
        log("Version:", version.strip())
        log("Email:", email.strip())
        log("Website:", website.strip())
        log("Describe:")
        log("".join(describe))
        log("INSTALL LIBS")
        pkglibs = pkgdat[pkgdat.index("# PKGLIBS #\n") + 1]
        for i in eval(pkglibs.strip()):
            pip.main(["install", i])
        log("UNPACK FILE...")
        if "// INITFILE //\n" in pkgdat:
            log("RUN INITFILE")
            filestart = pkgdat.index("// INITFILE //\n") + 1
            filestop = pkgdat.index("// INITFILE //\n", filestart)
            file = pkgdat[filestart:filestop]
            exec("".join(file))
        log("UNPACK CONTENT")
        log("LOCATE...")
        cstart = pkgdat.index("// CONTENT //\n") + 1
        cstop = pkgdat.index("// CONTENT //\n", cstart)
        contents = pkgdat[cstart:cstop]
        log("SPLIT FILE...")
        targets = []
        files = []
        for i in range(0, len(contents)):
            if contents[i] == "// START //\n":
                targets.append(i + 1)
            elif contents[i] == "// END //\n":
                targets.append(i)
        for i in range(0, len(targets), 2):
            files.append(contents[targets[i]:targets[i + 1]])
        for i in files:
            path, name = os.path.split(i[0].replace("> ", "").strip())
            if not os.path.exists(path):
                log(f"CREATE DIR {path}")
                os.makedirs(path)
            log(f"WRITE FILE {name}")
            with open(path + "/" + name, "w", encoding="utf-8") as f:
                f.write("".join(i[1:]))

    else:
        log("!!!ERROR EPKG FILE!!!")


def version12(pkgdat):
    if pkgdat[1].strip() == "/// EPKG DESCRIBE ///":
        log("PACK INFO")
        log(pkgdat[2].strip())
        log(pkgdat[3].strip())
        log(pkgdat[4].strip())
        log("DECODE ECODE...")
        ecstart = pkgdat.index("/// ECODE ///\n")
        ecstop = pkgdat.index("/// ECODE ///", ecstart)
        ecode = pkgdat[ecstart + 1:ecstop]
        rcode = base64.b64decode("".join(ecode).replace(" ", "").replace("\n", "")).decode("utf-8")
        pkgdat[ecstart:] = ""
        for i in rcode.splitlines():
            pkgdat.append(i + "\n")
        log("UNPACK EPKG...")
        infostart = pkgdat.index("// INFO //\n")
        infostop = pkgdat.index("// INFO //\n", infostart + 1)
        info = pkgdat[infostart + 1:infostop]
        name = info[info.index("# NAME #\n") + 1]
        author = info[info.index("# AUTHOR #\n") + 1]
        version = info[info.index("# VERSION #\n") + 1]
        email = info[info.index("# EMAIL #\n") + 1]
        website = info[info.index("# WEBSITE #\n") + 1]
        describe = info[info.index("# DESCRIBE #\n") + 1:info.index("## DESCRIBE ##\n")]
        log("Name:", name.strip())
        log("Author:", author.strip())
        log("Version:", version.strip())
        log("Email:", email.strip())
        log("Website:", website.strip())
        log("Describe:")
        log("".join(describe))
        log("INSTALL LIBS")
        pkglibs = pkgdat[pkgdat.index("# PKGLIBS #\n") + 1]
        for i in eval(pkglibs.strip()):
            pip.main(["install", i])
        log("UNPACK FILE...")
        if "// INITFILE //\n" in pkgdat:
            log("RUN INITFILE")
            filestart = pkgdat.index("// INITFILE //\n") + 1
            filestop = pkgdat.index("// INITFILE //\n", filestart)
            file = pkgdat[filestart:filestop]
            exec("".join(file))
        log("UNPACK CONTENT")
        log("LOCATE...")
        cstart = pkgdat.index("// CONTENT //\n") + 1
        cstop = pkgdat.index("// CONTENT //\n", cstart)
        contents = pkgdat[cstart:cstop]
        log("SPLIT FILE...")
        targets = []
        files = []
        for i in range(0, len(contents)):
            if contents[i] == "// START //\n":
                targets.append(i + 1)
            elif contents[i] == "// END //\n":
                targets.append(i)
        for i in range(0, len(targets), 2):
            files.append(contents[targets[i]:targets[i + 1]])
        for i in files:
            if i[0][0] == ">":
                path, name = os.path.split(i[0].replace("> ", "").strip())
                if not os.path.exists(path):
                    log(f"CREATE DIR {path}")
                    os.makedirs(path)
                log(f"WRITE FILE {name}")
                with open(path + "/" + name, "wb") as f:
                    f.write(eval("".join(i[1:])))
            elif i[0][0] == "+":
                path, name = os.path.split(i[0].replace("+ ", "").strip())
                if not os.path.exists(path):
                    log(f"CREATE DIR {path}")
                    os.makedirs(path)

    else:
        log("!!!ERROR EPKG FILE!!!")


def setup(path):
    with open(path, "r", encoding="utf-8") as f:
        pkgdat = f.readlines()
    if pkgdat[1].strip() == "/// EPKG DESCRIBE ///":
        version = pkgdat[2].strip().split(":")[1]
        log(pkgdat[2].strip())
        log("Try to unpack...")
        if version == "1.0":
            version10(pkgdat)
        elif version == "1.1":
            version11(pkgdat)
        elif version == "1.2":
            version12(pkgdat)
        else:
            log("Error Version")
    else:
        log("!!!ERROR EPKG FILE!!!")
