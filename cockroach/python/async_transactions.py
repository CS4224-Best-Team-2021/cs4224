import asyncio
import time

root = '~/temp/cs4224'

server

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

async def main(workload_type):
    await run(f'rm -rf {root}/cockroach/results && mkdir {root}/cockroach/results')
    txns = []
    for i in range(0, 40):
        txns.append(run(f'bash {root}/cockroach/app.sh < {root}/common/project_files_4/xact_files_{workload_type}/{i}.txt > {root}/cockroach/results/{i}_{workload_type}_result.txt'))

    await asyncio.gather(*txns)

# Since school server's Python version is 3.6.8, need to use older code
val = ''
while val != 'a' and val != 'b':
    val = input("Enter workload type (a/b):")
val = val.upper()

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(val))
loop.close()
end = time.time()
print(f"Number of seconds: {end - start}")