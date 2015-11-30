import random
import asyncio
import aiohttp

def linear_schedule(duration, start_rps, end_rps):
    schedule = []
    for i in range(duration):
        rps_this_sec = start_rps + (end_rps - start_rps) * i / duration
        step = 1. / rps_this_sec
        schedule += [i + (j + 1) * step for j in range(rps_this_sec)]
    return schedule

def constant_schedule(duration, rps):
    step = duration / rps
    return [(i + 1) * step for i in range(rps * duration)]

def join_schedule(schedules):
    final_schedule = schedules[0]
    for schedule in schedules[1:]:
        time_diff = final_schedule[-1]
        final_schedule += [time_diff + i for i in schedule]
    return final_schedule

loop = asyncio.get_event_loop()

class Tank:
    def __init__(self, schedule, requests, request_timeout=1):
        self.schedule = schedule
        self.requests = requests
        self.report = []
        self.request_timeout = request_timeout

    def save_report(self, start_time, end_time, http_code):
        self.report.append((start_time, end_time, http_code))

    async def run(self):
        start_time = loop.time()

        with aiohttp.ClientSession() as session:
            tasks = []

            for request_delay in self.schedule:
                time_to_sleep = request_delay - loop.time()
                if time_to_sleep > 0:
                    await asyncio.sleep(time_to_sleep)

                task = asyncio.ensure_future(self.send_request(request_delay, session))
                tasks.append(task)

            for task in tasks:
                await task

    async def send_request(self, request_schedule, session):
        with aiohttp.Timeout(self.request_timeout):
            try:
                async with session.get(random.choice(self.requests)) as rsp:
                    await rsp.text()
                    self.save_report(request_schedule, loop.time(), rsp.status)
            except (aiohttp.ClientError, asyncio.CancelledError) as e:
                self.save_report(request_schedule, loop.time(), -1)

if __name__ == "__main__":
    schedule = constant_schedule(5, 10)
    requests = ["http://github.com"]
    tank = Tank(schedule, requests)
    loop.run_until_complete(tank.run())
