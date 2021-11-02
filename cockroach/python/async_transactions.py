import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

async def main():
    txns = []
    for i in range(0, 2):
        txns.append(run(f'cat ~/temp/cs4224/common/project_files_4/xact_files_A/{i}.txt > {i}_result.txt'))

    await asyncio.gather(*txns)

# Since school server's Python version is 3.6.8, need to use older code
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()