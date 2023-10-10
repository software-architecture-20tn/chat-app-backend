# https://github.com/saritasa-nest/saritasa-python-invocations
from invoke import Collection
import saritasa_invocations

ns = Collection(
    saritasa_invocations.django,
    saritasa_invocations.docker,
    saritasa_invocations.pip,
    saritasa_invocations.pre_commit,
    saritasa_invocations.pytest,
    saritasa_invocations.open_api,
)

ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            pre_commit=saritasa_invocations.PreCommitSettings(
                hooks=(
                    "pre-commit",
                    "pre-push",
                    "commit-msg",
                )
            ),
            git=saritasa_invocations.GitSettings(
                merge_ff="true",
                pull_ff="only",
            ),
            docker=saritasa_invocations.DockerSettings(
                main_containers=("db", "redis"),
            ),
            system=saritasa_invocations.SystemSettings(
                vs_code_settings_template=".vscode/recommended_settings.json",
                settings_template="config/.env.local",
                save_settings_from_template_to="config/.env",
            ),
            # Default K8S Settings shared between envs
            # k8s_defaults=saritasa_invocations.K8SDefaultSettings(
            #     proxy="teleport.company.com",
            #     db_config=saritasa_invocations.K8SDBSettings(
            #         namespace="db",
            #         pod_selector="app=pod-selector-db",
            #     ),
            # ),
        ),
    },
)
