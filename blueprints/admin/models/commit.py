from ..utils import local_run

cmd = """git log --pretty=format:"%h;%an;%ad;%s" --abbrev-commit --date=short -n 30"""


class Commit:
    id = None
    message = None
    author = None
    when = None

    @staticmethod
    def gatherInfo():
        commits = []

        for output in local_run(cmd):
            for line in output.split('\n'):
                info = line.strip().split(';', 3)
                print "%s: %s" % (len(info), line)
                if len(info) == 4:
                    commit = Commit()
                    commit.id = info[0].decode("UTF-8")
                    commit.author = info[1].decode("UTF-8")
                    commit.when = info[2].decode("UTF-8")
                    commit.message = info[3].decode("UTF-8")
                    commits.append(commit)

        return commits