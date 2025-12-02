from autox.autox_logger import logger
from autox.utilities.common_utils import run_command


class Terraform:
    @staticmethod
    def terraform_run(main_cmd, tf_directory, tf_state_file=None, tf_vars=None):
        """
        main_cmd takes init or apply or destroy as argument
        """
        command = ["terraform", f"-chdir={tf_directory}", f"{main_cmd}", "-input=false", "-reconfigure"]

        if main_cmd == "apply" or main_cmd == "destroy":
            command.extend(f"-state={tf_state_file}")

        # Add variables if provided
        if tf_vars:
            command_variables = []

            for key, value in tf_vars.items():
                command_variables.append(f"-var={key}={value}")

            command.extend(command_variables)

        # Add auto approval, this is separate because we may or may not want this to be controllable
        command.append("-auto-approve")

        op_stdout, op_stderr = run_command(command)

        if op_stdout is None:
            logger.error("Terraform init operation aborted due to prior errors.")
            return

        if op_stderr:
            logger.warning(f"Terraform init had stderr output/warnings: {op_stderr}")

        logger.info("Terraform init successful:")
        logger.info(op_stdout)
