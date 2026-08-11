import os
from pathlib import Path
from subprocess import run

BASE_DIR = Path(__file__).resolve().parent


def check_root():
    certificates_path = BASE_DIR / "application" / "certificates"
    main_env_dir = BASE_DIR / "application"
    docker_env_dir = BASE_DIR / "docker"
    if not certificates_path.exists():
        os.mkdir(certificates_path)

    if not (certificates_path / "private-key.pem").exists():
        run(
            [
                "openssl",
                "genrsa",
                "-out",
                str(certificates_path / "private-key.pem"),
                "2048",
            ]
        )

    if not (certificates_path / "public-key.pem").exists():
        run(
            [
                "openssl",
                "rsa",
                "-in",
                str(certificates_path / "private-key.pem"),
                "-outform",
                "PEM",
                "-pubout",
                "-out",
                str(certificates_path / "public-key.pem"),
            ]
        )
    if not (main_env_dir / ".env").exists():
        run(
            [
                "cp",
                str(main_env_dir / ".env.example"),
                str(main_env_dir / ".env"),
            ]
        )
    if not (docker_env_dir / ".env").exists():
        run(
            ["cp", str(docker_env_dir/ ".env.example"), str(docker_env_dir / ".env")]
        )
        if not (docker_env_dir / "users.acl").exists():
            run(
                [
                    "cp",
                    str(docker_env_dir/ "users.acl.example"),
                    str(docker_env_dir/ "users.acl")
                ]
            )
    run(
        [
            "docker",
            "compose",
            "-f",
            str(docker_env_dir / "docker-compose.yaml"),
            "up",
            "-d",
            "--build",
        ]
    )


if __name__ == "__main__":
    check_root()
