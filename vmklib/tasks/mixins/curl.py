"""
A module for working with curl commands.
"""

# built-in
from asyncio import subprocess
from json import dumps
from typing import Any, Dict, Iterator, NamedTuple

# third-party
from vcorelib.asyncio.cli import handle_process_cancel
from vcorelib.task.subprocess.run import SubprocessLogMixin


class CommandResult(NamedTuple):
    """A container for a system command result."""

    code: int
    stdout: str
    stderr: str


def curl_headers(data: Dict[str, str]) -> Iterator[str]:
    """Get header arguments for curl based on some header data."""

    for key, value in data.items():
        yield "-H"
        yield f"{key}: {value}"


class CurlMixin(SubprocessLogMixin):
    """A task for generating ninja configurations."""

    async def curl(
        self,
        *args: str,
        post_data: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        method: str = None,
        entry: str = "curl",
        log: bool = True,
    ) -> CommandResult:
        """Run a curl command."""

        extra_args = []

        if post_data is not None:
            extra_args.extend(["-d", dumps(post_data)])
            if method is None:
                method = "POST"
            assert method == "POST"

        if method is not None:
            extra_args.extend(["-X", method])

        if headers is not None:
            extra_args.extend(list(curl_headers(headers)))

        proc, stdout, stderr = await handle_process_cancel(
            await self.subprocess_exec(
                entry,
                *extra_args,
                *args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            self.name,
            self.log,
        )

        assert proc.returncode is not None
        assert stdout is not None
        assert stderr is not None

        result = proc.returncode
        stdout_str = stdout.decode()
        stderr_str = stderr.decode()

        if log:
            self.logger.info(
                "%s result (%d) stdout='%s' stderr='%s'",
                entry,
                result,
                stdout_str,
                stderr_str,
            )

        return CommandResult(result, stdout_str, stderr_str)
