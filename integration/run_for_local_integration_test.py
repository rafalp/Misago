import subprocess


def main():
    subprocess.run(["docker-compose", "up", "-d", "--build", "community_app_web"])
    subprocess.run(["docker-compose", "exec", "community_app_web", "python3", "webapp/src/manage.py", "migrate"])


if __name__ == "__main__":
    main()
